# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

import copy
from django.conf import settings
from django.forms import model_to_dict
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.timezone import localtime, now
from django.utils.translation import ugettext
from django.views.generic import TemplateView

from _utils.views import LoginRequiredMixin, groupby_queryset_with_fields
from .models import Currency

current_date = localtime(now())


def get_transactions(queryset, start_date, end_date=current_date):
    queryset = queryset.filter(created__gte=start_date, created__lte=end_date)
    grouped_data = groupby_queryset_with_fields(queryset, ['transaction_type'])
    transactions = {}
    for data in grouped_data:
        for row in grouped_data[data]:
            transactions[row['grouper'].lower()] = row['list']
    return transactions


class DashboardIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'currency/index.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardIndexView, self).get_context_data(**kwargs)
        user = self.request.user

        context['currencies'] = []
        for currency in Currency.objects.all():
            cur = model_to_dict(currency)
            cur.update({'current_rate': currency.get_current_rate()})
            cur.update({'get_per_month': currency.get_per_month(cur['current_rate'])})
            context['currencies'].append(cur)
        context['total_balance'] = user.get_total_balance()
        context['transaction'] = get_transactions(user.user_transactions.all(), current_date - timedelta(days=7))
        return context


class CurrencyDataView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return JsonResponse(context['json'], status=200)

    def get_context_data(self, **kwargs):
        context = super(CurrencyDataView, self).get_context_data(**kwargs)
        currency_code = self.request.GET.get('currency_code')
        context['json'] = {'labels': [], 'data': []}
        try:
            currency = Currency.objects.get(code=currency_code)
            for data in currency.get_per_month()['rates']:
                context['json']['labels'].append(str(data.created.date()))
                context['json']['data'].append(float(data.price))
        except Currency.DoesNotExist:
            pass
        return context


class TransactionDataView(LoginRequiredMixin, TemplateView):
    template_name = 'ajax/transaction.html'

    def get(self, request, *args, **kwargs):
        response = super(TransactionDataView, self).get(request, *args, **kwargs)
        user = request.user
        days = int(request.GET.get('days', 0))
        total_balance = user.get_total_balance()
        if not days:
            return JsonResponse({'error': ugettext('No. of days required')}, status=400)

        graph_days = copy.copy(settings.GRAPH_DAYS)
        graph_days.remove(days)
        transaction = get_transactions(user.user_transactions.all(), current_date - timedelta(days=days))
        payload = render_to_string(self.template_name, context={'transaction': transaction,
                                                                'total_balance': total_balance,
                                                                'days':days,
                                                                'remaining_days':graph_days})
        return JsonResponse({'payload': payload}, status=200)
