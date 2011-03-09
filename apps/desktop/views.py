import datetime

from django.shortcuts import get_object_or_404

from spark.decorators import login_required

from users.models import User, Profile

import jingo


def home(request):
    if request.user.is_authenticated():
        d = datetime.datetime(2011, 2, 18)
        profile = request.user.profile
        delta = datetime.datetime.now() - profile.user.date_joined
        return jingo.render(request, 'desktop/dashboard.html',
                                    {'username': profile.user.username,
                                     'profile': profile,
                                     'logged_in': True,
                                     'levels': profile.challenge_info,
                                     'date_joined_delta': _total_seconds(delta) })
    else:
        return jingo.render(request, 'desktop/home.html', {'is_homepage': True})


def user(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    delta = datetime.datetime.now() - user.date_joined
    data = {'username': username,
            'profile': user.profile,
            'logged_in': request.user.is_authenticated(),
            'date_joined_delta': _total_seconds(delta),
            'is_user_page': True}
    
    return jingo.render(request, 'desktop/user.html', data)


def visualization(request, ):
    return jingo.render(request, 'desktop/visualization.html', {})


@login_required
def ajax_pwchange(request):
    return jingo.render(request, 'desktop/home.html', {})


@login_required
def ajax_delaccount(request):
    return jingo.render(request, 'desktop/home.html', {})


def _total_seconds(td):
    """Returns the total number of seconds in a given timedelta."""
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6