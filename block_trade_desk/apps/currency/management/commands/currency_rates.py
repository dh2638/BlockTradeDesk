import json
from decimal import Decimal

import requests
from django.core.management.base import BaseCommand

from apps.currency.models import Currency, CurrencyPerHourRate


class Command(BaseCommand):
    def handle(self, database="default", *args, **options):
        currencies = Currency.objects.all()
        API_URL = 'https://api.cryptonator.com/api/ticker/{0}-{1}'
        target_currency = 'usd'
        for currency in currencies:
            data = requests.get(API_URL.format(currency.code.lower(), target_currency))
            content = json.loads(data.content)
            if data.status_code == 200 and content['success']:
                kwargs = {
                    'currency': currency,
                    'price': Decimal(content['ticker']['price']),
                    'target_currency': target_currency,
                    'change': Decimal(content['ticker']['change']),
                    'timestamp': content['timestamp']
                }
                CurrencyPerHourRate.objects.create(**kwargs)
        self.stdout.write(self.style.SUCCESS('Updated every currency prices in database'))
