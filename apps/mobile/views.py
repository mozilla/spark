from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse as django_reverse
from django.utils.http import urlquote

import jingo

from spark.models import City
from spark.urlresolvers import reverse, absolute_url
from spark.decorators import post_required, json_view
from spark.utils import (get_city_fullname, is_supported_non_firefox, is_iphone,
                         is_firefox_mobile, is_android, get_ua, approximate_major_city,
                         get_country_name)

from users.models import User, UserNode
from users.utils import create_relationship

from challenges.tasks import update_completed_challenges
from challenges.models import Challenge
from challenges.utils import get_badge_name

from desktop.views import home as desktop_home

from sharing.utils import set_sharing_cookies
from sharing.messages import (TWITTER_SHARE_MSG, TWITTER_SPARK_MSG, TWITTER_BADGE_MSG, 
                              FACEBOOK_SPARK_TITLE, FACEBOOK_SPARK_MSG, FACEBOOK_BADGE_MSG)

from stats.models import SharingHistory, CountrySparked, CitySharingHistory
from stats.utils import get_global_stats

from .forms import BoostStep1Form, BoostStep2Form
from .decorators import login_required, logout_required

from tower import ugettext as _, ugettext_lazy as _lazy



def home(request):
    if request.user.is_authenticated():
        profile = request.user.profile
        return jingo.render(request, 'mobile/myspark.html', 
                                    {'profile': profile})

    data = {}
    if is_firefox_mobile(request):
        template = 'mobile/home.html'
    elif is_iphone(request):
        template = 'mobile/iphone.html'
    else:
        data.update({'non_supported': not is_supported_non_firefox(request)})
        template = 'mobile/non_firefox.html'
    
    return jingo.render(request, template, data)


@login_required
def boost(request):
    profile = request.user.profile

    # 'Boost your Spark' is not available once both steps have been completed
    if profile.boost2_completed and profile.boost1_completed:
        return HttpResponseRedirect(reverse('mobile.home'))

    return jingo.render(request, 'mobile/boost.html')


@login_required
@json_view
def boost1(request):
    """ Boost your Spark step 1/2 :
        Allows a Spark user to be geolocated by the application."""
    profile = request.user.profile
    
    if profile.boost1_completed:
        return HttpResponseRedirect(reverse('mobile.boost2'))
    
    data = {}
    if request.method == 'POST':
        form = BoostStep1Form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            profile.latitude = data['lat']
            profile.longitude = data['long']
            profile.city_name = data['city']
            profile.country_code = data['country_code']
            if data['country_code'] == 'US':
                profile.us_state = data['us_state']
            profile.boost1_completed = True
            profile.save()
            
            approximate_major_city(profile, 1000)
            
            CountrySparked.add_country(data['country_code'])

            update_completed_challenges.delay(profile.user.id)
            
            profile.add_city_shares_for_children()
            
            return HttpResponseRedirect(reverse('mobile.boost1_complete'))
        else:
            data.update({'geolocation': 'error'})

    return jingo.render(request, 'mobile/boost_step1.html', data)


@login_required
def boost1_complete(request):
    profile = request.user.profile
    if not profile.boost1_completed:
        return HttpResponseRedirect(reverse('mobile.boost1'))
    
    return jingo.render(request, 'mobile/boost_step1.html', {'geolocation': 'success',
                'geo_result': get_city_fullname(profile.city_name, profile.country_code, request.locale)})


@login_required
@json_view
def geolocation_fallback(request):
    ajax = request.is_ajax()
    profile = request.user.profile
    if not profile.boost1_completed:
        
        if request.method == 'POST':
            city_id = request.POST.get('city')
    
            try:
                city = City.objects.get(pk=city_id)
                profile.major_city = city
                profile.latitude = city.latitude
                profile.longitude = city.longitude
                profile.city_name = city.city_name
                profile.country_code = city.country_code
                profile.boost1_completed = True
                profile.save()
                
                CountrySparked.add_country(city.country_code)
                
                update_completed_challenges.delay(profile.user.id)
                
                profile.add_city_shares_for_children()
                
                if ajax:
                    return {'status': 'success', 
                            'data': {'cityName': profile.city_name,
                                     'countryName': get_country_name(profile.country_code, request.locale)}}
                else:
                    return HttpResponseRedirect(reverse('mobile.boost1_complete'))
            except City.DoesNotExist:
                # Wrong city in the POST data
                if ajax:
                    return {'status': 'error',
                            'errors': {'citylist': [_('Select your location manually')]}}
    
        cities = City.objects.order_by('city_name')
        citylist = [(city.id, get_city_fullname(city.city_name, city.country_code, request.locale)) for city in cities]

        return jingo.render(request, 'mobile/citylist.html', {'cities': citylist})
    
    # Ignore chosen city and redirect if user has already completed Boost step 1.
    return HttpResponseRedirect(reverse('mobile.boost1_complete'))


@login_required
@json_view
def boost2(request):
    """ Boost your Spark step 2/2 :
        Allows a Spark user to find a parent user by username or email address."""
    profile = request.user.profile
    ajax = request.is_ajax()

    if profile.boost2_completed:
        return HttpResponseRedirect(reverse('mobile.home'))

    if request.method == 'POST':
        form = BoostStep2Form(request.user, request.POST)
        if form.is_valid():
            data = {}
            if form.parent_username:
                data.update({'parent': form.parent_username})
            else: # User just checked the 'I started a new Spark on my own' box
                data.update({'no_parent': True})
            
            if ajax:
                return {'status': 'success', 'data': data}
            else:
                return jingo.render(request, 'mobile/boost_step2_found.html', data)
        else:
            if ajax:
                return {'status': 'error',
                        'errors': dict([(k, [unicode(e) for e in v]) for k,v in form.errors.items()])}
    else:
        form = BoostStep2Form(request.user)
    
    return jingo.render(request, 'mobile/boost_step2.html', {'form': form})


@login_required
@post_required
@json_view
def boost2_confirm(request):
    """ Boost your Spark step 2/2 confirmation.
        This view saves the parent-child relationship in the user tree.
    """
    profile = request.user.profile
    ajax = request.is_ajax()
    
    if profile.boost2_completed:
        return HttpResponseRedirect(reverse('mobile.home'))
    
    username = request.POST.get('parent')
    no_parent = request.POST.get('no_parent')
    if username or no_parent:
        error = False
        if not no_parent:
            try:
                parent = User.objects.get(username=username)
                created = create_relationship(parent, request.user)
                
                if created:
                    profile.no_parent = False
                    profile.save()
                    
                    # Update 'longest chain' stat of all ancestors if necessary
                    profile.update_ancestors_longest_chain()
                    
                    # Add a share for the parent
                    SharingHistory.add_share(parent.profile)
                    
                    # Add a share between cities of this user and the parent user
                    CitySharingHistory.add_share_from_profiles(parent.profile, profile)
                    
                    # Trigger challenge completion for the parent
                    update_completed_challenges.delay(parent.id)
                else:
                    error = True
            except User.DoesNotExist:
                error = True
        
        if not error:
            profile = request.user.profile
            profile.parent_username = username
            profile.boost2_completed = True
            profile.save()
            
            # Don't use a celery task here so that "+{n} new" notification
            # has the correct value in the mobile menu on the next page.
            # This requires to award badges synchronously for this particular step.
            update_completed_challenges(profile.user.id)
            
            if ajax:
                return {'status': 'success', 'url': reverse('desktop.parent_info')}
            else:
                return HttpResponseRedirect(reverse('mobile.home'))
        else:
            if ajax:
                return {'status': 'error'}
    
    return jingo.render(request, 'spark/handlers/mobile/400.html', status=400)


@login_required
def badges(request):
    profile = request.user.profile
    data = {'profile': profile, 'badges': profile.badges}
    if len([b for b in data['badges'] if b['new']]) > 0:
        profile.clear_new_badges()
    
    return jingo.render(request, 'mobile/badges.html', data)


@login_required
def challenges(request):
    profile = request.user.profile
    if profile.new_challenges:
        profile.clear_new_challenges()
        
    return jingo.render(request, 'mobile/challenges.html', 
                                        {'profile': profile,
                                         'levels': profile.challenge_info})


def instructions(request):
    return jingo.render(request, 'mobile/instructions.html')


@login_required
def stats(request):
    return jingo.render(request, 'mobile/stats.html', {'stats': get_global_stats()})


@login_required
def shareqr(request):
    return jingo.render(request, 'mobile/shareqr.html')


@login_required
def sharelink(request):
    data = {'twitter_url': urlquote(request.user.profile.twitter_sharing_url),
            'twitter_msg': urlquote(unicode(TWITTER_SPARK_MSG)),
            'facebook_url': request.user.profile.facebook_sharing_url,
            'facebook_redirect': absolute_url(django_reverse('mobile.home')),
            'facebook_title': urlquote(unicode(FACEBOOK_SPARK_TITLE)),
            'facebook_spark_msg': urlquote(unicode(FACEBOOK_SPARK_MSG))}
            
    return jingo.render(request, 'mobile/sharelink.html', data)


@login_required
def sharebadge(request):
    badge_id = request.GET.get('id')
    try:
        # Verify that this badge exists
        badge = Challenge.objects.get(pk=badge_id)
        
        # Verify also that this user has earned this badge
        profile = request.user.profile
        has_badge = profile.has_badge(badge_id)
        
        if has_badge:
            data = {'badge_name': get_badge_name(badge.id),
                    'twitter_url': urlquote(profile.twitter_sharing_url),
                    'twitter_badge_msg': TWITTER_BADGE_MSG,
                    'facebook_url': profile.facebook_sharing_url,
                    'facebook_redirect': absolute_url(django_reverse('mobile.home')),
                    'facebook_title': urlquote(unicode(FACEBOOK_SPARK_TITLE)),
                    'facebook_badge_msg': FACEBOOK_BADGE_MSG }
            return jingo.render(request, 'mobile/sharebadge.html', data)
    except Challenge.DoesNotExist:
        # Ignore invalid badges
        pass
    
    # Return to earned badges page if the querystring contains an invalid badge id
    # or if the user tried to share a badge he/she has not earned yet.
    return HttpResponseRedirect(reverse('mobile.badges'))


def about(request):
    return jingo.render(request, 'mobile/about.html')


def legal(request):
    return jingo.render(request, 'mobile/legal.html')


def iphone(request):
    return jingo.render(request, 'mobile/iphone.html')


def non_android(request):
    return jingo.render(request, 'mobile/non_firefox.html', {'non_supported': True})


def non_firefox(request):
    return jingo.render(request, 'mobile/non_firefox.html')


def user(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    via = request.GET.get('f')
    data = {'username': username,
            'profile': user.profile,
            'logged_in': request.user.is_authenticated(),
            'supported_non_ff': is_supported_non_firefox(request),
            'iphone': is_iphone(request),
            'firefox': is_firefox_mobile(request)}

    response = jingo.render(request, 'mobile/user.html', data)
    return set_sharing_cookies(response, username, via)


def visualization(request):
    from django.http import HttpResponse
    from stats.tasks import update_aggregate_history
    import json

    return HttpResponse(json.dumps(update_aggregate_history()), mimetype='application/json')
