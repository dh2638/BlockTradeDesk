# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView

from _utils.views import LoginRequiredMixin, groupby_queryset_with_fields
from .models import Currency


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
        current_date = timezone.now().date()
        queryset = user.user_transactions.filter(created__date__gte=current_date - timedelta(days=30))
        grouped_data = groupby_queryset_with_fields(queryset, ['transaction_type'])
        transactions = {}
        for data in grouped_data:
            for row in grouped_data[data]:
                transactions[row['grouper'].lower()] = row['list']
        context['transactions'] = transactions
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
