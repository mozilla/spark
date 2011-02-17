from spark.urlresolvers import reverse

import jingo

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
    return jingo.render(request, 'mobile/boost_step2.html', {})


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
    return jingo.render(request, 'mobile/about.html', {})


def legal(request):
    return jingo.render(request, 'mobile/legal.html', {})