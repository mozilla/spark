from datetime import datetime

from django.shortcuts import get_object_or_404

from spark.decorators import login_required

from users.models import User, Profile

import jingo


def home(request):
    if request.user.is_authenticated():
        d = datetime(2011, 2, 18)
        profile = request.user.profile
        return jingo.render(request, 'desktop/dashboard.html', {'username': profile.user.username,
                                                                'profile': profile,
                                                                'logged_in': True, 
                                                                'levels': profile.challenge_info})
    else:
        return jingo.render(request, 'desktop/home.html', {'is_homepage': True})


def user(request, username):
    user_profile = get_object_or_404(Profile, user__username=username)
    data = {'username': username,
            'profile': user_profile,
            'logged_in': request.user.is_authenticated(),
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