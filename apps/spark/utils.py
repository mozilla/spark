import re
import math


def is_mobile_request(request):
    mobile_url = re.compile(r'.+/m/.+')
    return mobile_url.match(request.path) != None


# Author: Wayne Dyck
# http://www.platoscave.net/blog/2009/oct/5/calculate-distance-latitude-longitude-python/
def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


def approximate_city(profile, radius):
    """
    Finds the closest major city to the user's lat/long in a given km radius.
    Updates the user profile if a major city is found.
    """
    from geo.cities import cities
    from spark.models import City
    
    nearest = None
    min_distance = 0
    for (name, props) in cities.iteritems():
        user_pos = (profile.latitude, profile.longitude)
        city_pos = (props['lat'], props['lng'])
        d = abs(distance(user_pos, city_pos))
        if (d < min_distance or not nearest) and d <= radius:
            min_distance = d
            nearest = name
    
    if nearest:
        profile.major_city = City.objects.get(pk=nearest)
        profile.save()