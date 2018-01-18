# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView

from _utils.views import LoginRequiredMixin, groupby_queryset_with_fields
from .models import Currency


class DashboardIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'currency/index.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardIndexView, self).get_context_data(**kwargs)
        user = self.request.user
        context['currencies'] = Currency.objects.all()
        context['total_balance'] = user.get_total_balance()
        grouped_data = groupby_queryset_with_fields(user.user_transactions.all(), ['transaction_type'])
        transactions = {}
        for data in grouped_data:
            for row in grouped_data[data]:
                transactions[row['grouper'].lower()] = row['list']
        context['transactions'] = transactions
        return context
