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


def get_city_fullname(city, locale):
    from geo.countries import countries
    
    if not city:
        return ''
    
    if locale not in countries:
        locale = 'en-US'
    
    cc = city.country_code.lower()
    if cc in countries[locale]:
        country = countries[locale][cc]
    else:
        return '?'
    
    return '%s, %s' % (city.city_name, country)


def get_ua(request):
    return request.META.get('HTTP_USER_AGENT', '')


def is_iphone(request):
    return 'iPhone' in get_ua(request)


def is_android_non_firefox(request):
    ua = get_ua(request)
    if 'Android' in ua and not 'Firefox' in ua:
        return True
    return False


def is_firefox_mobile(request):
    ua = get_ua(request)
    if 'Android' in ua and 'Firefox' in ua:
        return True
    return False


def is_mobile(request):
    return is_iphone(request) or is_android_non_firefox(request) or is_firefox_mobile(request)
