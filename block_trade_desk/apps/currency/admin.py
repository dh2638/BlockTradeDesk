# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Currency, UserCurrency, Transaction, CurrencyPerDayRate, CurrencyPerHourRate


class UserCurrencyAdmim(admin.ModelAdmin):
    list_display = ('user', 'currency', 'amount')


class CurrencyPerHourRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'target_currency', 'price', 'created')


class CurrencyPerDayRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'target_currency', 'price', 'created')


admin.site.register(Currency)
admin.site.register(UserCurrency, UserCurrencyAdmim)
admin.site.register(Transaction)
admin.site.register(CurrencyPerDayRate, CurrencyPerDayRateAdmin)
admin.site.register(CurrencyPerHourRate, CurrencyPerHourRateAdmin)
