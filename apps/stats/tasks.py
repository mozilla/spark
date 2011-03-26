import datetime

from django.conf import settings
from django.db.models import Count, Q

from celery.decorators import task

from users.models import User, Profile
from spark.models import City

from .models import CitySharingHistory


NUM_STEPS = 300

@task
def update_aggregate_history():
    return get_aggregate_history(-1)


@task
def update_user_history(user_id):
    return get_aggregate_history(user_id)


def get_aggregate_history(user_id):
    start = settings.CAMPAIGN_STARTING_DATE
    delta = datetime.datetime.now() - start
    step_duration = delta / NUM_STEPS
    
    profile = None
    if user_id != -1:
        try:
            user = User.objects.get(pk=user_id, is_active=True)
            profile = user.profile
        except Profile.DoesNotExist:
            pass
    
    all_shares = []
    share_counts = {}
    city_positions = get_ordered_cities()
    
    for i in xrange(NUM_STEPS):
        step_start_date = start + (i * step_duration)
        step_end_date = start + ((i+1) * step_duration)
        
        if profile:
            criteria = Q(date_shared__gt=step_start_date, date_shared__lte=step_end_date, sharer=profile)
        else:
            criteria = Q(date_shared__gt=step_start_date, date_shared__lte=step_end_date)
        
        shares = (CitySharingHistory.objects.filter(criteria)
                                            .values('city_from', 'city_to')
                                            .annotate(share_count=Count('city_from')))
        
        step_shares = []
        for s in shares:
            city1 = int(s['city_from'])
            city2 = int(s['city_to'])
            sid = '%d-%d' % (city1, city2)
            
            if share_counts.get(sid):
                share_counts[sid] += s['share_count']
            else:
                share_counts[sid] = s['share_count']
            
            step_shares.append([city_positions[city1], city_positions[city2], share_counts[sid]])
        
        all_shares.append(step_shares if step_shares else [])

    return all_shares



def get_final_history(user_id):
    city_positions = get_ordered_cities()
    
    profile = None
    if user_id != -1:
        try:
            user = User.objects.get(pk=user_id, is_active=True)
            profile = user.profile
        except Profile.DoesNotExist:
            pass
    
    if profile:
        shares = (CitySharingHistory.objects.filter(sharer=profile)
                                            .values('city_from', 'city_to')
                                            .annotate(share_count=Count('city_from')))
    else:
        shares = (CitySharingHistory.objects.values('city_from', 'city_to')
                                        .annotate(share_count=Count('city_from')))
    
    final_history = []
    for s in shares:
        final_history.append([city_positions[int(s['city_from'])], city_positions[int(s['city_to'])], s['share_count']])
    
    return final_history


def get_ordered_cities():
    cities = City.objects.order_by('longitude').all()
    cities_ordered = {}
    
    for (i, c) in enumerate(cities):
        cities_ordered[int(c.id)] = i+1
    
    return cities_ordered



