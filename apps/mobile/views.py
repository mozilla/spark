from spark.urlresolvers import reverse

from django.http import HttpResponseRedirect

import jingo

from users.models import User

from .forms import BoostStep2Form
from .decorators import login_required, logout_required


def home(request):
    if request.user.is_authenticated():
        return jingo.render(request, 'mobile/myspark.html', {})
    return jingo.render(request, 'mobile/home.html', {})


@login_required
def boost(request):
    return jingo.render(request, 'mobile/boost.html', {})


@login_required
def boost1(request):
    return jingo.render(request, 'mobile/boost_step1.html', {})


@login_required
def boost2(request):
    """ Boost your Spark step 2/2 :
        Allows a Spark user to link his account to a parent user."""
    if request.method == 'POST':
        form = BoostStep2Form(request.user, request.POST)
        if form.is_valid():
            return jingo.render(request, 'mobile/boost_step2_found.html',
                                        {'parent': form.parent_username})
    else:
        form = BoostStep2Form(request.user)
    
    return jingo.render(request, 'mobile/boost_step2.html', {'form': form})


@login_required
def boost2_confirm(request):
    """ Boost your Spark step 2/2 completion. """
    parent = None
    username = request.GET.get('parent')
    
    if username:
        parent = User.objects.filter(username=username)
    
    if parent:
        return HttpResponseRedirect(reverse('mobile.home'))
    else:
        return jingo.render(request, 'spark/handlers/mobile/400.html', status=400)


@login_required
def badges(request):
    badgelist = range(8)
    return jingo.render(request, 'mobile/badges.html', { 'badges': badgelist })


@login_required
def challenges(request):
    return jingo.render(request, 'mobile/challenges.html', {})


def instructions(request):
    return jingo.render(request, 'mobile/instructions.html', {})


@login_required
def stats(request):
    return jingo.render(request, 'mobile/stats.html', {})


@login_required
def shareqr(request):
    return jingo.render(request, 'mobile/shareqr.html', {})


@login_required
def sharelink(request):
    return jingo.render(request, 'mobile/sharelink.html', {})


def about(request):
    return jingo.render(request, 'mobile/about.html')


def legal(request):
    return jingo.render(request, 'mobile/legal.html')