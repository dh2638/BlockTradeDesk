# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView

from .models import Currency


class DashboardIndexView(TemplateView):
    template_name = 'currency/index.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardIndexView, self).get_context_data(**kwargs)
        context['currencies'] = Currency.objects.all()



        return context
