from django.conf.urls import url

from .views import DashboardIndexView, CurrencyDataView, TransactionDataView

urlpatterns = [
    url(r'^$', DashboardIndexView.as_view(), name='index'),
    url(r'^currency/data/$', CurrencyDataView.as_view(), name='currency_data'),
    url(r'^transaction/data/$', TransactionDataView.as_view(), name='transation_data'),
]
