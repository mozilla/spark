from datetime import datetime

from django.shortcuts import get_object_or_404

from spark.decorators import login_required

from users.models import User

import jingo


def home(request):
    return jingo.render(request, 'desktop/home.html', { 'is_homepage': True })


@login_required
def dashboard(request):
    d = datetime(2011, 2, 18)
    profile = request.user.profile
    return jingo.render(request, 'desktop/dashboard.html', { 'logged_in': True,
                                                             'profile': profile,
                                                             'most_recent_share': d,
                                                             'badges': profile.badges,
                                                             'levels': profile.challenge_info })


def user(request, username):
    d = datetime(2011, 2, 18)
    user_profile = get_object_or_404(Profile, user__username=username)
    return jingo.render(request, 'desktop/user.html', { 'profile': user_profile,
                                                        'logged_in': request.user.is_authenticated(),
                                                        'is_user_page': True,
                                                        'most_recent_share': d })


def visualization(request, ):
    return jingo.render(request, 'desktop/visualization.html', {})


@login_required
def ajax_pwchange(request):
    return jingo.render(request, 'desktop/home.html', {})


@login_required
def ajax_delaccount(request):
    return jingo.render(request, 'desktop/home.html', {})