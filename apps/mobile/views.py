from django.http import HttpResponseRedirect

import jingo

from spark.urlresolvers import reverse
from spark.decorators import post_required

from users.models import User

from .forms import BoostStep1Form, BoostStep2Form
from .decorators import login_required, logout_required



def home(request):
    if request.user.is_authenticated():
        return jingo.render(request, 'mobile/myspark.html', {})
    return jingo.render(request, 'mobile/home.html', {})


@login_required
def boost(request):
    profile = request.user.get_profile()

    # 'Boost your Spark' is not available once both steps have been completed
    if profile.boost2_completed and profile.boost1_completed:
        return HttpResponseRedirect(reverse('mobile.home'))

    return jingo.render(request, 'mobile/boost.html')


@login_required
def boost1(request):
    """ Boost your Spark step 1/2 :
        Allows a Spark user to be geolocated by the application."""
    profile = request.user.get_profile()
    
    if profile.boost1_completed:
        return HttpResponseRedirect(reverse('mobile.boost2'))
    
    data = {}
    if request.method == 'POST':
        form = BoostStep1Form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            profile.latitude = data['lat']
            profile.longitude = data['long']
            #profile.city = data['city']
            profile.boost1_completed = True
            profile.save()
            data.update({'geolocation': 'success',
                         'geo_result': '%s, %s' % (data['city'], data['country'])})
        else:
            data.update({'geolocation': 'error'})
        
    return jingo.render(request, 'mobile/boost_step1.html', data)


@login_required
def boost2(request):
    """ Boost your Spark step 2/2 :
        Allows a Spark user to link his account to a parent user."""
    profile = request.user.get_profile()

    if profile.boost2_completed:
        return HttpResponseRedirect(reverse('mobile.boost2'))

    if request.method == 'POST':
        form = BoostStep2Form(request.user, request.POST)
        if form.is_valid():
            data = {}
            if form.parent_username:
                data.update({'parent': form.parent_username})
            else: # User just checked the 'I started a new Spark on my own' box
                data.update({'no_parent': True})
            
            return jingo.render(request, 'mobile/boost_step2_found.html', data)
    else:
        form = BoostStep2Form(request.user)
    
    return jingo.render(request, 'mobile/boost_step2.html', {'form': form})


@login_required
@post_required
def boost2_confirm(request):
    """ Boost your Spark step 2/2 completion. """
    username = request.POST.get('parent')
    if username:
        parent_user = User.objects.filter(username=username) 
        if parent_user:
            return HttpResponseRedirect(reverse('mobile.home'))
    
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


@login_required
def sharebadge(request):
    return jingo.render(request, 'mobile/sharebadge.html', {})


def about(request):
    return jingo.render(request, 'mobile/about.html')


def legal(request):
    return jingo.render(request, 'mobile/legal.html')


def iphone(request):
    return jingo.render(request, 'mobile/iphone.html')


def non_android(request):
    return jingo.render(request, 'mobile/non_firefox.html', {'non_android': True})


def non_firefox(request):
    return jingo.render(request, 'mobile/non_firefox.html')


def user(request):
    return jingo.render(request, 'mobile/user.html', {'num_people': 8, 
                                                      'num_countries': 5,
                                                      'num_badges': 9})
