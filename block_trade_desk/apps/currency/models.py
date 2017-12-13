# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

UserModel = get_user_model()
SOLD, BOUGHT = "SOLD", "BOUGHT"
TRANSACTION_TYPES = (
    (SOLD, SOLD),
    (BOUGHT, BOUGHT)
)


class Currency(TimeStampedModel):
    name = models.CharField(_('Currency Name'), max_length=255)
    code = models.CharField(_('Short Code'), max_length=20)

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

    def __unicode__(self):
        return self.name

    def get_current_rate(self):
        return self.rates_per_hour.first().price

    def get_per_month(self):
        time_threshold = timezone.now() - datetime.timedelta(days=30)
        month_rates = self.rates_per_day.filter(created__gte=time_threshold)
        last_rate = month_rates.last()
        if last_rate.price < self.get_current_rate():
            percent = (self.get_current_rate() / last_rate.price) % 100
            is_negative = False
        else:
            percent = (last_rate.price / self.get_current_rate()) % 100
            is_negative = True

        kwargs = {'rates': month_rates, 'duration': 'since last month', 'last_rate': last_rate.price,
                  'percent': "%.2f" % percent, 'is_negative': is_negative}
        # if len(month_rates) != 30:
        #     kwargs['duration'] = "since {0} day(s)".format(len(month_rates))
        return kwargs

    def get_per_day(self):
        current_date = timezone.now().date()
        today_rates = self.rates_per_hour.filter(created__date=current_date)
        kwargs = {'rates': today_rates}
        return kwargs



        # Monthly Graph


class CurrencyPerDayRate(TimeStampedModel):
    currency = models.ForeignKey(Currency, related_name='rates_per_day')
    price = models.DecimalField(max_digits=16, decimal_places=8)
    target_currency = models.CharField(max_length=10, default='USD')
    change = models.DecimalField(max_digits=16, decimal_places=8, default=Decimal("0.0"))

    class Meta:
        verbose_name = _('Currency Rate')
        verbose_name_plural = _('Currency Rates')
        ordering = ['-created']

    def __unicode__(self):
        return "{0}".format(self.price)


class CurrencyPerHourRate(TimeStampedModel):
    currency = models.ForeignKey(Currency, related_name='rates_per_hour')
    price = models.DecimalField(max_digits=16, decimal_places=8)
    target_currency = models.CharField(max_length=10, default='USD')
    change = models.DecimalField(max_digits=16, decimal_places=8, default=Decimal("0.0"))
    timestamp = models.IntegerField()

    class Meta:
        verbose_name = _('Currency Rate')
        verbose_name_plural = _('Currency Rates')
        ordering = ['-created']

    def __unicode__(self):
        return "{0}".format(self.price)


class UserCurrency(TimeStampedModel):
    user = models.ForeignKey(UserModel, related_name='user_currencies')
    currency = models.ForeignKey(Currency, related_name='user_currencies')
    amount = models.DecimalField(max_digits=16, decimal_places=8, default=Decimal("0.0"))

    class Meta:
        verbose_name = _('User Currency')
        verbose_name_plural = _('User Currencies')

    def __unicode__(self):
        return "{0}".format(self.amount)


class Transaction(TimeStampedModel):
    user = models.ForeignKey(UserModel, related_name='user_transactions')
    transaction_type = models.CharField(_('Transaction Type'), choices=TRANSACTION_TYPES, max_length=255)
    amount = models.DecimalField(max_digits=16, decimal_places=8, default=Decimal("0.0"))
    currency = models.ForeignKey(Currency, related_name='currency_transaction')
    message = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _('Transaction')

    def __unicode__(self):
        return "{0} {1} {2}".format(self.transaction_type, self.amount, self.message)
