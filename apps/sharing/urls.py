from django.conf.urls.defaults import patterns, url

from spark.views import redirect_to
from . import views

urlpatterns = patterns('',
    url(r'^download/qr$', views.download_from_qr_redirect, name='sharing.download'),
    url(r'^download/market$', views.download_from_market_desktop, name='sharing.download_from_market_desktop'),
    url(r'^m/download/market$', views.download_from_market_mobile, name='sharing.download_from_market_mobile')
)