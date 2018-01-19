from django.conf.urls import url

from .views import DashboardIndexView, CurrencyDataView

urlpatterns = [
    url(r'^$', DashboardIndexView.as_view(), name='index'),
    url(r'^currency/data/$', CurrencyDataView.as_view(), name='currency_data'),
]
