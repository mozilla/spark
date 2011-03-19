import json

from django.conf import settings
from django.http import (HttpResponsePermanentRedirect, HttpResponseRedirect,
                         HttpResponse)

import jingo

from spark.urlresolvers import reverse
from spark.utils import is_mobile_request
from spark.decorators import ajax_required

from stats.models import SharingHistory

from users.models import User

from .utils import set_parent_cookie


DOWNLOAD_URL = 'http://firefox.com/m/'


def download(request):
    username = request.GET.get('user')
    via = request.GET.get('via')
    
    if username:
        try:
            user = User.objects.get(username=username)
            if via:
                SharingHistory.add_share_from_qr_code(user.profile)
        except User.DoesNotExist:
            # Ignore unknown usernames
            pass
    
    return HttpResponseRedirect(DOWNLOAD_URL)


@ajax_required
def download_from_market_desktop(request):
    response = HttpResponse(json.dumps({'next': 'http://market.android.com/details?id=org.mozilla.firefox'}),
                            content_type='application/json')
    return _handle_tracking(request, response)


@ajax_required
def download_from_market_mobile(request):
    response = HttpResponse(json.dumps({'next': 'market://details?id=org.mozilla.firefox'}),
                            content_type='application/json')
    return _handle_tracking(request, response)


def _handle_tracking(request, response):
    """Handles the share tracking logic so that users get their number of shares increased
       when someone downloads Firefox mobile via their user page."""
    if not _has_parent_cookie(request):
        parent_username = _add_share_to_parent(request)
        # Set a 'parent' cookie so that you can't trigger a +1 share for the parent more than once.
        response = set_parent_cookie(response, parent_username)
    
    return response


def _has_parent_cookie(request):
    """The 'parent' cookie is set when the user clicks on the Download button.
       This is to prevent users from cheating and clicking multiple times on their
       own button to gain more shares.
    """
    return 'parent' in request.COOKIES
    

def _add_share_to_parent(request):
    username = request.COOKIES.get('shared_by', None)
    if username:
        try:
            user = User.objects.get(username=username)
            SharingHistory.add_share(user.profile)
            
            return username
        except User.DoesNotExist:
            # Ignore 'shared_by' cookies if they have been tampered with
            # or if the parent user has deleted their account in the meantime.
            pass

    return None
