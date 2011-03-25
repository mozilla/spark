from datetime import date
import urllib2

from django.utils.http import urlencode
from django.conf import settings


def make_source_url(request):
    return request.get_host() + request.get_full_path()

def subscribe(campaigns, address, format='html', source_url='', lang=''):
    for campaign in campaigns:
        data = {
            'LANG_LOCALE': lang,
            'SOURCE_URL': source_url,
            'EMAIL_ADDRESS_': address,
            'EMAIL_FORMAT_': 'H' if format == 'html' else 'T',
            }
        
        data['%s_FLG' % campaign] = 'Y'
        data['%s_DATE' % campaign] = date.today().strftime('%Y-%m-%d')
        data['_ri_'] = settings.RESPONSYS_ID

        try:
            res = urllib2.urlopen(settings.RESPONSYS_URL, data=urlencode(data))
            if res.code != 200:
                return False
        except urllib2.URLError, e:
            return False

    return True