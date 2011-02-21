from django.shortcuts import get_object_or_404

from spark.decorators import login_required

from users.models import Profile

import jingo


def home(request):
    return jingo.render(request, 'desktop/home.html', { 'is_homepage': True })


#@login_required
def dashboard(request):
    return jingo.render(request, 'desktop/dashboard.html', { 'logged_in': True })


def user(request, username):
    user_profile = get_object_or_404(Profile, user__username=username)
    return jingo.render(request, 'desktop/user.html', { 'profile': user_profile,
                                                        'logged_in': request.user.is_authenticated(),
                                                        'is_user_page': True })


@login_required
def ajax_pwchange(request):
    return jingo.render(request, 'desktop/home.html', {})


@login_required
def ajax_delaccount(request):
    return jingo.render(request, 'desktop/home.html', {})