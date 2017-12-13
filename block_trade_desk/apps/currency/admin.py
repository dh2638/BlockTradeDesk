# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Currency, UserCurrency, Transaction


class UserCurrencyAdmim(admin.ModelAdmin):
    list_display = ('user', 'currency', 'amount')


admin.site.register(Currency)
admin.site.register(UserCurrency, UserCurrencyAdmim)
admin.site.register(Transaction)
