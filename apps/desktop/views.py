import datetime
import json

from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse as django_reverse
from django.utils.http import urlquote

from geo.countries import countries

from spark.decorators import ssl_required, login_required, mobile_view
from spark.helpers import secure_url
from spark.urlresolvers import reverse, absolute_url
from spark.utils import get_city_fullname

from sharing.utils import set_sharing_cookies
from sharing.messages import (TWITTER_SHARE_MSG, TWITTER_SPARK_MSG, FACEBOOK_SPARK_TITLE, 
                              FACEBOOK_SPARK_MSG, FACEBOOK_SHARE_MSG)

from spark.urlresolvers import absolute_url

from users.models import User, Profile

from stats.utils import get_global_stats

import jingo


@ssl_required
@mobile_view('mobile.home')
def home(request):
    if request.user.is_authenticated():
        profile = request.user.profile
        delta = datetime.datetime.now() - profile.user.date_joined
        return jingo.render(request, 'desktop/dashboard.html',
                                    {'username': profile.user.username,
                                     'profile': profile,
                                     'logged_in': True,
                                     'levels': profile.challenge_info,
                                     'date_joined_delta': _total_seconds(delta),
                                     'countries': json.dumps(countries[request.locale]),
                                     'sparked_countries': json.dumps(profile.sparked_countries),
                                     'twitter_url': urlquote(profile.twitter_sharing_url),
                                     'twitter_msg': urlquote(unicode(TWITTER_SPARK_MSG)),
                                     'facebook_url': profile.facebook_sharing_url,
                                     'facebook_redirect': absolute_url(django_reverse('desktop.close_popup')),
                                     'facebook_title': urlquote(unicode(FACEBOOK_SPARK_TITLE)),
                                     'facebook_spark_msg': urlquote(unicode(FACEBOOK_SPARK_MSG)),
                                     'abs_url': profile.generic_sharing_url,
                                     'stats': get_global_stats()})
    else:
        data = {'is_homepage': True,
                'twitter_url': urlquote(absolute_url(django_reverse('desktop.home'))),
                'twitter_msg': urlquote(unicode(TWITTER_SHARE_MSG)),
                'facebook_url': absolute_url(django_reverse('desktop.home')),
                'facebook_redirect': absolute_url(django_reverse('desktop.close_popup')),
                'facebook_msg': urlquote(unicode(FACEBOOK_SHARE_MSG)),
                'facebook_title': urlquote(unicode(FACEBOOK_SPARK_TITLE)),
                'stats': get_global_stats()}
        return jingo.render(request, 'desktop/home.html', data)


@ssl_required
@mobile_view('mobile.user')
def user(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    via = request.GET.get('f')
    delta = datetime.datetime.now() - user.date_joined
    data = {'username': username,
            'profile': user.profile,
            'logged_in': request.user.is_authenticated(),
            'date_joined_delta': _total_seconds(delta),
            'is_user_page': True,
            'countries': json.dumps(countries[request.locale]),
            'sparked_countries': json.dumps(user.profile.sparked_countries),
            'twitter_url': urlquote(user.profile.twitter_sharing_url),
            'twitter_msg': urlquote(unicode(TWITTER_SHARE_MSG)),
            'facebook_url': user.profile.facebook_sharing_url,
            'facebook_redirect': absolute_url(django_reverse('desktop.home')),
            'facebook_title': urlquote(unicode(FACEBOOK_SPARK_TITLE)),
            'facebook_spark_msg': urlquote(unicode(FACEBOOK_SPARK_MSG)),
            'stats': get_global_stats()}
    
    if not request.user.is_authenticated():
        data.update({'login_next_url': request.path})

    response = jingo.render(request, 'desktop/user.html', data)
    return set_sharing_cookies(response, username, via)


def visualization(request):
    from spark.models import City
    from stats.tasks import get_ordered_cities
    from stats.tasks import get_aggregate_history, get_final_history
    import json
    
    cities_by_name = City.objects.order_by('city_name').all()
    positions = get_ordered_cities()
    
    cities_by_longitude = City.objects.order_by('longitude')
    citylist = json.dumps([get_city_fullname(c.city_name, c.country_code, request.locale) for c in cities_by_longitude])
    
    data = {'cities': [(positions[c.id], get_city_fullname(c.city_name, c.country_code, request.locale)) for c in cities_by_name],
            'citylist': citylist,
            'share_history': get_aggregate_history(-1),
            'final_history': get_final_history(-1),
            'starting_date': _timestamp(settings.CAMPAIGN_STARTING_DATE)}
    
    if request.user.is_authenticated():
        data.update({'logged_in': True,
                     'user_history': get_aggregate_history(request.user.id),
                     'user_final_history': get_final_history(request.user.id) })
    else:
        data.update({'login_next_url': reverse('desktop.visualization')})
    
    return jingo.render(request, 'desktop/visualization.html', data)


def close(request):
    return jingo.render(request, 'desktop/close.html')
    
    
def _total_seconds(td):
    """Returns the total number of seconds in a given timedelta."""
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
    
def _timestamp(d):
    return _total_seconds(d - datetime.datetime(1970, 1, 1)) * 1000