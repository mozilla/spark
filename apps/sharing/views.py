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



DESKTOP_DOWNLOAD_URL = 'http://market.android.com/details?id=org.mozilla.firefox'
MOBILE_DOWNLOAD_URL = 'market://details?id=org.mozilla.firefox'


def download_from_qr_redirect(request):
    username = request.GET.get('user', None)
    
    response = HttpResponseRedirect(MOBILE_DOWNLOAD_URL)
    
    if not _has_parent_cookie(request):
        parent_username = _add_share_to_user(request, username, 'qr')
        if parent_username:
            # Set a 'parent' cookie so that you can't trigger a +1 share for the parent more than once.
            response = set_parent_cookie(response, parent_username)

    return response


@ajax_required
def download_from_market_desktop(request):
    response = HttpResponse(json.dumps({'next': DESKTOP_DOWNLOAD_URL}),
                            content_type='application/json')
    return _handle_tracking(request, response)


@ajax_required
def download_from_market_mobile(request):
    response = HttpResponse(json.dumps({'next': MOBILE_DOWNLOAD_URL}),
                            content_type='application/json')
    return _handle_tracking(request, response)


def _handle_tracking(request, response):
    """Handles the share tracking logic so that users get their number of shares increased
       when someone downloads Firefox mobile via their user page."""
    if not _has_parent_cookie(request):
        parent_username = _add_share_from_cookies(request)
        # Set a 'parent' cookie so that you can't trigger a +1 share for the parent more than once.
        response = set_parent_cookie(response, parent_username)
    
    return response


def _has_parent_cookie(request):
    """The 'parent' cookie is set when the user clicks on the Download button.
       This is to prevent users from cheating and clicking multiple times on their
       own button to gain more shares.
    """
    return 'parent' in request.COOKIES
    

def _add_share_from_cookies(request):
    username = request.COOKIES.get('shared_by', None)
    via = request.COOKIES.get('via', None)
    if username:
        return _add_share_to_user(request, username, via)

    return None


def _trigger_challenge_detection(username):
    from challenges.tasks import update_completed_challenges

    user = User.objects.get(username=username, is_active=True)
    update_completed_challenges.delay(user.id)


def _add_share_to_user(request, username, via):
    try:
        user = User.objects.get(username=username)
        tz_offset = request.GET.get('tz', None)
        
        if via ==  't':
            SharingHistory.add_share_from_twitter(user.profile, tz_offset)
        elif via == 'fb':
            SharingHistory.add_share_from_facebook(user.profile, tz_offset)
        elif via == 'qr':
            SharingHistory.add_share_from_qr_code(user.profile, tz_offset)
        elif via == 'p':
            SharingHistory.add_share_from_poster(user.profile, tz_offset)
        else:
            SharingHistory.add_share(user.profile, tz_offset)
        
        # Gaining a share triggers detection of completed challenges
        _trigger_challenge_detection(username)
        
        return username
    except User.DoesNotExist:
        # Ignore 'shared_by' cookies if they have been tampered with
        # or if the parent user has deleted their account in the meantime.
        return None


