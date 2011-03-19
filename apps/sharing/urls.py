from django.conf.urls.defaults import patterns, url

from spark.views import redirect_to
from . import views

urlpatterns = patterns('',
    url(r'^download$', views.download, name='sharing.download'),
    url(r'^download/market$', views.download_from_market, name='sharing.download_from_market')
)