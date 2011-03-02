from datetime import date
import urllib2

from django.utils.http import urlencode

try:
    from django.conf import settings
except ImportError:
    settings = {}

try:
    if settings.RESPONSYS_URL:
        URL = settings.RESPONSYS_URL
except AttributeError:
    #URL = 'http://awesomeness.mozilla.org/pub/rf'
    pass

def make_source_url(request):
    return request.get_host() + request.get_full_path()

def subscribe(campaigns, address, format='html', source_url='', lang=''):
    data = {
        'LANG_LOCALE': lang,
        'SOURCE_URL': source_url,
        'EMAIL_ADDRESS_': address,
        'EMAIL_FORMAT_': 'H' if format == 'html' else 'T',
        }
    
    for campaign in campaigns:
        data['%s_FLG' % campaign] = 'Y'
        data['%s_DATE' % campaign] = date.today().strftime('%Y-%m-%d')

    # views.py asserts setting is available
    data['_ri_'] = settings.RESPONSYS_ID
    try:
        if settings.DEBUG:
            for d in data:
                print '%s -> %s' % (d, data[d])
        res = urllib2.urlopen(URL, data=urlencode(data))
        return res.code == 200
    except urllib2.URLError, e:
        return False
