import datetime
import json

from django.conf import settings
from django.shortcuts import get_object_or_404

from geo.countries import countries

from spark.decorators import ssl_required, login_required, mobile_view
from spark.helpers import secure_url

from sharing.utils import set_shared_by_cookie

from users.models import User, Profile

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
                                     'countries': json.dumps(countries[request.locale]) })
    else:
        return jingo.render(request, 'desktop/home.html', {'is_homepage': True})


@ssl_required
@mobile_view('mobile.user')
def user(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    delta = datetime.datetime.now() - user.date_joined
    data = {'username': username,
            'profile': user.profile,
            'logged_in': request.user.is_authenticated(),
            'date_joined_delta': _total_seconds(delta),
            'is_user_page': True,
            'countries': json.dumps(countries[request.locale]) }

    response = jingo.render(request, 'desktop/user.html', data)
    return set_shared_by_cookie(response, username)


def visualization(request, ):
    return jingo.render(request, 'desktop/visualization.html', {})


@login_required
def ajax_pwchange(request):
    return jingo.render(request, 'desktop/home.html', {})


@login_required
def ajax_delaccount(request):
    return jingo.render(request, 'desktop/home.html', {})


def test_celery(request):
    from django.http import HttpResponse
    from .tasks import a_test_task
    
    try:
        a_test_task.delay(1)
    except Exception, e:
        return HttpResponse("<html><body>Celery is not working<br>Error: %s</body></html>" % e)
    
    return HttpResponse("<html><body>Celery is working</body></html>")

def test_celery2(request):
    import sys, traceback
    from django.http import HttpResponse
    from challenges.tasks import update_completed_challenges
    from users.models import User

    try:
        username = request.GET.get('user')
        user = User.objects.get(username=username)
        update_completed_challenges.delay(user.id)
    except Exception, e:
        type, value, tb = sys.exc_info()
        stacktrace = '%s:%s<br>%s' % (type.__name__, value, '<br>'.join(traceback.format_tb(tb)))
        return HttpResponse("<html><body>Error:<p>%s</body></html>" % stacktrace)

    return HttpResponse("<html><body>Challenge completion task has been scheduled for %s</body></html>" % username)
    


def _total_seconds(td):
    """Returns the total number of seconds in a given timedelta."""
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6