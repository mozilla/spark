from django.conf.urls.defaults import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^poster/(?P<username>[\w.+-]+)/spark-poster.pdf$', views.userposter, name='poster.userposter')
)