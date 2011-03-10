from django.conf.urls.defaults import patterns, url

from spark.views import redirect_to
from . import views

urlpatterns = patterns('',
    url(r'^download$', views.download, name='sharing.download'),
)