import time
import urllib2

from django.utils.http import cookie_date

from users.models import User


def url2qr(url, size=150):
    API = 'https://chart.googleapis.com/chart?chs=%dx%d&cht=qr&chl=%s&chld=L|1'
    return API % (size, size, urllib2.quote(url))


def set_sharing_cookies(response, username, service):
    response = set_via_cookie(response, service)
    response = set_shared_by_cookie(response, username)
    return response


def set_shared_by_cookie(response, username):
    if _username_exists(username):
        return _set_cookie(response, 'shared_by', username, 3600)
    else:
        # Don't set cookie if username is unknown
        return response


def set_via_cookie(response, via):
    if via in ['t', 'fb', 'qr', 'p']: # Twitter, Facebook, QR code, Poster
        return _set_cookie(response, 'via', via, 3600)
    else:
        # Don't set cookie if via argument is invalid
        return response


def set_parent_cookie(response, username):
    return _set_cookie(response, 'parent', username, 3600 * 24 * 90)


def _set_cookie(response, name, value, duration):
    max_age = duration
    expires_time = time.time() + max_age
    expires = cookie_date(expires_time)
    response.set_cookie(name,
                        value,
                        max_age=max_age,
                        expires=expires)
    return response


def _username_exists(username):
    try:
        User.objects.get(username=username, is_active=True)
        return True
    except User.DoesNotExist:
        return False