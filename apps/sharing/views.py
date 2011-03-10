from django.conf import settings

from django.http import (HttpResponsePermanentRedirect, HttpResponseRedirect,
                         HttpResponse)

import jingo

from spark.urlresolvers import reverse
from spark.utils import is_mobile_request

from stats.models import SharingHistory

from users.models import User


DOWNLOAD_URL = 'http://firefox.com/m/'


def download(request):
    username = request.GET.get('user')
    via = request.GET.get('via')
    
    if username:
        user_profile = User.objects.get(username=username).profile
        if via:
            SharingHistory.add_share_from_qr_code(user_profile)
    
    return HttpResponseRedirect(DOWNLOAD_URL)
