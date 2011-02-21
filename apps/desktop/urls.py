from django.conf.urls.defaults import patterns, url

from spark.views import redirect_to
from . import views

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': 'desktop.home'}),
    url(r'^home$', views.home, name='desktop.home'),
    url(r'^dashboard$', views.dashboard, name='desktop.dashboard'),
    url(r'^user/(?P<username>[\w\d]+)$', views.user, name='desktop.user'),
    
    url(r'^pwchange', views.ajax_pwchange, name='desktop.pwchange'),
    url(r'^delaccount', views.ajax_delaccount, name='desktop.delaccount'),
)