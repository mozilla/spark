import re
import math



def is_mobile_request(request):
    mobile_url = re.compile(r'.+/m/.+')
    return mobile_url.match(request.path) != None


# Slightly modified version of function by Wayne Dyck
# http://www.platoscave.net/blog/2009/oct/5/calculate-distance-latitude-longitude-python/
def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    if lat1 and lon1 and lat2 and lon2:
        dlat = math.radians(float(lat2) - float(lat1))
        dlon = math.radians(float(lon2) - float(lon1))
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
    else:
        d = -1

    return d


def get_nearest_city(lat, lon, radius):
    from spark.models import City
    
    nearest = None
    min_distance = 0
    for city in City.objects.all():
        user_pos = (lat, lon)
        city_pos = (city.latitude, city.longitude)
        d = abs(distance(user_pos, city_pos))
        if (d < min_distance or not nearest) and d <= radius:
            min_distance = d
            nearest = city
    
    return nearest
    

def approximate_major_city(profile, radius):
    """
    Finds the closest major city to the user's lat/long within a given km radius.
    Updates the user profile if a major city is found.
    """
    nearest = get_nearest_city(profile.latitude, profile.longitude, radius)
    
    if nearest:
        profile.major_city = nearest
        profile.save()


def get_country_name(country_code, locale):
    from geo.countries import countries
    
    cc = country_code.lower()
    if cc in countries[locale]:
        country_name = countries[locale][cc]
    else:
        country_name = '?'
    
    return country_name


def get_city_fullname(city_name, country_code, locale):
    from geo.countries import countries
    
    if locale not in countries:
        locale = 'en-US'
    
    country_name = get_country_name(country_code, locale)
    
    return '%s, %s' % (city_name, country_name)


def get_ua(request):
    return request.META.get('HTTP_USER_AGENT', '')


def is_iphone(request):
    return 'iPhone' in get_ua(request)


def is_android(request):
    ua = get_ua(request)
    if 'Android' in ua:
        return True
    return False


def is_supported_non_firefox(request):
    ua = get_ua(request)
    if ('Android' in ua or 'Maemo' in ua) and not 'Firefox' in ua:
        return True
    return False


def is_firefox_mobile(request):
    ua = get_ua(request)
    if ('Android' in ua or 'Maemo' in ua) and 'Firefox' in ua:
        return True
    return False


def is_mobile(request):
    return is_iphone(request) or is_supported_non_firefox(request) or is_firefox_mobile(request)
