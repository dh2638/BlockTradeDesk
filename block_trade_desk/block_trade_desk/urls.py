from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import *
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

router = DefaultRouter()


def bad(request):
    """ Simulates a server error """
    1 / 0

# Website URL
import debug_toolbar

urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))]
urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bad/$', bad),
    url(r'^dashboard/', include('apps.currency.urls', namespace='dashboard')),
    url(r'^django-rq/', include('django_rq.urls')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^', include('accounts.urls', namespace='accounts')),
    url(r'^', include('cms.urls')),

]

if settings.DEBUG:
    urlpatterns += [
        # Testing 404 and 500 error pages
        url(r'^404/$', TemplateView.as_view(template_name='404.html'), name='404'),
        url(r'^500/$', TemplateView.as_view(template_name='500.html'), name='500'),
    ]

    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


