from django.conf.urls.defaults import patterns, url

from spark.views import redirect_to
from . import views

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': 'desktop.home'}),
    url(r'^home$', views.home, name='desktop.home'),
    url(r'^user/(?P<username>[\w.+-]+)$', views.user, name='desktop.user'),
    url(r'^global$', views.visualization, name='desktop.visualization'),
    url(r'^close$', views.close, name='desktop.close_popup'),
    url(r'^cities$', views.cities, name='desktop.cities'),
    url(r'^location_info$', views.home_location_info, name='desktop.location_info'),
    url(r'^parent_info$', views.parent_user_info, name='desktop.parent_info'),
    url(r'^challenges$', views.ajax_challenges, name='desktop.ajax_challenges'),
    url(r'^badges$', views.ajax_badges, name='desktop.ajax_badges'),
)