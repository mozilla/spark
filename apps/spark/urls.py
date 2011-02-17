from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^robots.txt$', direct_to_template, {'template': 'spark/robots.html',  'mimetype': 'text/plain'}),
)