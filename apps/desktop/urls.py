from django.conf.urls.defaults import patterns, url

from spark.views import redirect_to
from . import views

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': 'desktop.home'}),
    url(r'^home$', views.home, name='desktop.home'),
    url(r'^user/(?P<username>[\w.@+-]+)$', views.user, name='desktop.user'),
    url(r'^global$', views.visualization, name='desktop.visualization'),
    
    url(r'^pwchange', views.ajax_pwchange, name='desktop.pwchange'),
    url(r'^delaccount', views.ajax_delaccount, name='desktop.delaccount'),
    
    ### Temporary - Celery test
    url(r'^test_celery$', views.test_celery, name='desktop.test_celery'),
    url(r'^test_celery2$', views.test_celery2, name='desktop.test_celery2'),
)