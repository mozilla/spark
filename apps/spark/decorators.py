import json

from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import (HttpResponse, HttpResponseForbidden, HttpResponseRedirect,
                         HttpResponseBadRequest, HttpResponseNotAllowed)
from django.utils.decorators import available_attrs
from django.utils.http import urlquote
from django.utils.encoding import smart_str

from .helpers import urlparams
from .urlresolvers import reverse


def mobile_view(mobile_view_name):
    """This decorator redirects the view to a mobile view if request.MOBILE == True."""
    def decorator(view_fn):
        @wraps(view_fn)
        def wrapper(request, *args, **kw):
            if request.MOBILE:
                query = dict((smart_str(k), request.GET[k]) for k in request.GET)
                return HttpResponseRedirect(urlparams(reverse(mobile_view_name, args=kw.values()), **query))
            else:
                return view_fn(request, *args, **kw)
        return wrapper
    return decorator


## Taken from kitsune & zamboni

def ssl_required(view_func):
    """A view decorator that enforces HTTPS.

    If settings.DEBUG is True, it doesn't enforce anything."""
    def _checkssl(request, *args, **kwargs):
        if not settings.DEBUG and not request.is_secure():
            url_str = request.build_absolute_uri()
            url_str = url_str.replace('http://', 'https://')
            return HttpResponseRedirect(url_str)

        return view_func(request, *args, **kwargs)
    return _checkssl


def user_access_decorator(redirect_func, redirect_url_func, deny_func=None,
                          redirect_field=REDIRECT_FIELD_NAME, mobile=False):
    """
    Helper function that returns a decorator.

    * redirect func ----- If truthy, a redirect will occur
    * deny_func --------- If truthy, HttpResponseForbidden is returned.
    * redirect_url_func - Evaluated at view time, returns the redirect URL
                          i.e. where to go if redirect_func is truthy.
    * redirect_field ---- What field to set in the url, defaults to Django's.
                          Set this to None to exclude it from the URL.

    """
    def decorator(view_fn):
        def _wrapped_view(request, *args, **kwargs):
            if redirect_func(request.user):
                # We must call reverse at the view level, else the threadlocal
                # locale prefixing doesn't take effect.
                if mobile:
                    default_login_url = reverse('users.mobile_login')
                else:
                    default_login_url = reverse('users.login')
                
                redirect_url = redirect_url_func() or default_login_url

                # Redirect back here afterwards?
                if redirect_field:
                    path = urlquote(request.get_full_path())
                    redirect_url = '%s?%s=%s' % (
                        redirect_url, redirect_field, path)

                return HttpResponseRedirect(redirect_url)

            if deny_func and deny_func(request.user):
                return HttpResponseForbidden()

            return view_fn(request, *args, **kwargs)
        return wraps(view_fn, assigned=available_attrs(view_fn))(_wrapped_view)

    return decorator


def logout_required(redirect, mobile=False):
    """Requires that the user *not* be logged in."""
    redirect_func = lambda u: u.is_authenticated()
    if hasattr(redirect, '__call__'):
        home_view = 'mobile.home' if mobile else 'desktop.home'
        return user_access_decorator(
            redirect_func, redirect_field=None,
            redirect_url_func=lambda: reverse(home_view))(redirect)
    else:
        return user_access_decorator(redirect_func, redirect_field=None,
                                     redirect_url_func=lambda: redirect)


def login_required(func, login_url=None, redirect=REDIRECT_FIELD_NAME,
                   only_active=True, mobile=False):
    """Requires that the user is logged in."""
    if only_active:
        redirect_func = lambda u: not (u.is_authenticated() and u.is_active)
    else:
        redirect_func = lambda u: not u.is_authenticated()
    redirect_url_func = lambda: login_url
    return user_access_decorator(redirect_func, redirect_field=redirect,
                                 redirect_url_func=redirect_url_func,
                                 mobile=mobile)(func)

def post_required(f):
    @wraps(f)
    def wrapper(request, *args, **kw):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])
        else:
            return f(request, *args, **kw)
    return wrapper


def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """    
    def wrap(request, *args, **kwargs):
            if not request.is_ajax():
                return HttpResponseBadRequest()
            return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap


def json_view(f):
    @wraps(f)
    def wrapper(*args, **kw):
        response = f(*args, **kw)
        if isinstance(response, HttpResponse):
            return response
        else:
            return HttpResponse(json.dumps(response),
                                    content_type='application/json')
    return wrapper

json_view.error = lambda s: http.HttpResponseBadRequest(
    json.dumps(s), content_type='application/json')


