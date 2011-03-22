import datetime

from django.db.models import Count, Q

from celery.decorators import task

from users.models import User, Profile
from spark.models import City

from .models import CitySharingHistory


NUM_STEPS = 300

@task
def update_aggregate_history():
    return _get_aggregate_history(-1)


@task
def update_user_history(user_id):
    return _get_aggregate_history(user_id)


def _get_aggregate_history(user_id):
    start = datetime.datetime(2011, 3, 9)
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
    city_positions = _ordered_cities()
    
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


@task
def update_final_history():
    city_positions = _ordered_cities()
    
    shares = (CitySharingHistory.objects.values('city_from', 'city_to')
                                        .annotate(share_count=Count('city_from')))
    
    final_history = []
    for s in shares:
        final_history.append([city_positions[int(s['city_from'])], city_positions[int(s['city_to'])], s['share_count']])
    
    return final_history


def _ordered_cities():
    cities = City.objects.order_by('longitude').all()
    cities_ordered = {}
    
    for (i, c) in enumerate(cities):
        cities_ordered[int(c.id)] = i+1
    
    return cities_ordered


def _generate_fake_history():
    import random
    
    CitySharingHistory.objects.all().delete()
    
    ordered_cities = _ordered_cities()
    
    start = datetime.datetime(2011, 3, 9)
    
    city_pairs = [(4, 97), (45, 127), (128, 128), (22, 114), (99, 286), (54, 58), (124, 201), (15, 43), (3, 305), (67, 67),
                  (59, 75), (289, 308), (89, 168), (145, 273), (178, 241), (164, 164), (38, 297), (87, 116), (78, 230), (27, 90),
                  (10, 100), (29, 100), (100, 100), (100, 212), (100, 218), (100, 275), (100, 112), (34, 300), (27, 79), (2, 143),
                  (15, 17), (87, 201), (83, 232), (140, 255), (241, 315), (78, 90), (145, 178), (69, 156), (128, 199), (78, 78),
                  (54, 82), (69, 69), (280, 280), (12, 12), (116, 116), (66, 187), (146, 164), (239, 305), (67, 90), (2, 79),
                  (15, 127), (29, 201), (140, 187), (12, 66), (239, 275), (66, 146), (18, 67), (128, 156), (1, 269), (1, 316)]
    
    cities_qs = City.objects.order_by('longitude').all()
    cities_positions = {}
    for (i, c) in enumerate(cities_qs):
      cities_positions[i+1] = int(c.id)
    
    def random_city_pair():
        return city_pairs[random.randint(0, len(city_pairs)-1)]
    
    t = start
    while t < datetime.datetime.now():
        t += datetime.timedelta(minutes=random.randint(1,10))
        city1_pos, city2_pos = random_city_pair()
        
        city1 = City.objects.get(pk=cities_positions[city1_pos])
        city2 = City.objects.get(pk=cities_positions[city2_pos])

        user_id = 3
        if (city1_pos == 100 or city2_pos == 100) and random.randint(1,3) == 3:
            user_id = 4

        profile = User.objects.get(pk=user_id).profile
        
        share = CitySharingHistory.objects.create(city_from=city1,
                                                  city_to=city2,
                                                  sharer=profile)
        share.date_shared = t
        share.save()
