from django.conf.urls.defaults import patterns, url

from spark.views import redirect_to
from . import views

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': 'mobile.home'}),
    url(r'^home$', views.home, name='mobile.home'),
    url(r'^badges$', views.badges, name='mobile.badges'),
    url(r'^challenges$', views.challenges, name='mobile.challenges'),
    url(r'^instructions$', views.instructions, name='mobile.instructions'),
    url(r'^stats$', views.stats, name='mobile.stats'),
    url(r'^share/qr$', views.shareqr, name='mobile.shareqr'),
    url(r'^share/link$', views.sharelink, name='mobile.sharelink'),
    url(r'^about$', views.about, name='mobile.about'),
    url(r'^legal$', views.legal, name='mobile.legal'),
    url(r'^boost$', views.boost, name='mobile.boost'),
    url(r'^boost1$', views.boost1, name='mobile.boost1'),
    url(r'^boost2$', views.boost2, name='mobile.boost2'),
    url(r'^boost2_confirm$', views.boost2_confirm, name='mobile.boost2_confirm'),
    url(r'^user$', views.user, name='mobile.user'),
    url(r'^iphone$', views.iphone, name='mobile.home_iphone'),
    url(r'^non-android$', views.non_android, name='mobile.home_non_android'),
    url(r'^non-ff$', views.non_firefox, name='mobile.home_non_firefox'),
)