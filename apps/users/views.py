import os
import urlparse
import json

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.forms import (PasswordResetForm, SetPasswordForm,
                                       PasswordChangeForm, AuthenticationForm)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, 
                         Http404)
from django.views.decorators.http import require_http_methods, require_GET
from django.shortcuts import get_object_or_404
from django.utils.http import base36_to_int

import jingo

from spark.urlresolvers import reverse
from spark.helpers import url

from spark.decorators import (ssl_required, logout_required, login_required, 
                              post_required, json_view, ajax_required)

from users.backends import Sha256Backend
from users.forms import (EmailConfirmationForm, EmailChangeForm)
from users.models import Profile
from users.utils import handle_login, handle_register

try:
    if True == settings.CELERY_ENABLED:
        from responsys import responsys_async as responsys
    else:
        from responsys import responsys
except AttributeError:
    from responsys import responsys



@ssl_required
@json_view
def login(request, mobile=False):
    """Try to log the user in."""
    form = handle_login(request)
    
    if mobile:
        next_url = _clean_next_url(request) or reverse('mobile.home')
        
        if request.user.is_authenticated():
            return HttpResponseRedirect(next_url)

        return jingo.render(request, 'users/mobile/login.html',
                            {'form': form, 'next_url': next_url})
    else: # ajax login
        if request.method == 'POST' and request.is_ajax():
            if not form.is_valid():
                return {'status': 'error',
                        'errors': dict(form.errors.iteritems())}
            else:
                return {'status': 'success',
                        'next': reverse('desktop.home')}

        return HttpResponseBadRequest()


@ssl_required
def logout(request, mobile=False):
    """Log the user out."""
    auth.logout(request)
    next_url = _clean_next_url(request) if 'next' in request.GET else ''
    home_view = 'mobile.home' if mobile else 'desktop.home'
    return HttpResponseRedirect(next_url or reverse(home_view))


@ssl_required
@logout_required
@require_http_methods(['GET', 'POST'])
def register(request):
    """Register a new user."""
    form = handle_register(request)
    if form.is_valid():
        data = form.cleaned_data
        optins = []
        if data['newsletter']:
            optins.append(settings.MOZILLA_CAMPAIGN)
        if data['spark_newsletter']:
            optins.append(settings.SPARK_CAMPAIGN)
        
        if len(optins) > 0:
            status= responsys.subscribe(optins,
                                        data['email'],
                                        'html',
                                        responsys.make_source_url(request),
                                        request.locale)
        
        return HttpResponseRedirect(reverse('mobile.home'))
    return jingo.render(request, 'users/mobile/register.html',
                        {'form': form})


@login_required
@post_required
@ajax_required
@json_view
def change_email(request):
    """Change user's email"""
    form = EmailChangeForm(request.user, request.POST)
    u = request.user
    if form.is_valid() and u.email != form.cleaned_data['new_email']:
        return {'new_email': form.cleaned_data['new_email']}
        
    return {'email': request.user.email}


@json_view
def password_reset(request, mobile=False):
    """Password reset form.

    Based on django.contrib.auth.views. This view sends the email.

    """
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(use_https=request.is_secure(),
                      token_generator=default_token_generator,
                      email_template_name='users/email/pw_reset.ltxt')
        
        # Don't leak existence of email addresses 
        # (No error if wrong email address)
        if mobile:
            return HttpResponseRedirect(reverse('users.mobile_pw_reset_sent'))
        else:
            return {'pw_reset_sent': True}
    else:
        form = PasswordResetForm()

    if mobile:
        return jingo.render(request, 'users/mobile/pw_reset_form.html', {'form': form})
#    else:
#        return http.HttpResponse(json.dumps(response),
#                                content_type='application/json')


def password_reset_sent(request):
    """Password reset email sent.

    Based on django.contrib.auth.views. This view shows a success message after
    email is sent.

    """
    return jingo.render(request, 'users/mobile/pw_reset_sent.html')


@ssl_required
@json_view
def password_reset_confirm(request, uidb36=None, token=None, mobile=False):
    """View that checks the hash in a password reset link and presents a
    form for entering a new password.

    Based on django.contrib.auth.views.

    """
    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, id=uid_int)
    context = {}

    if default_token_generator.check_token(user, token):
        context['validlink'] = True
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                if mobile:
                    return HttpResponseRedirect(reverse('users.mobile_pw_reset_complete'))
                else:
                    return {'pw_reset_complete': True}
        else:
            form = SetPasswordForm(None)
    else:
        context['validlink'] = False
        form = None
    context['form'] = form

    return jingo.render(request, 'users/mobile/pw_reset_confirm.html', context)


def password_reset_complete(request):
    """Password reset complete.
    """
    return jingo.render(request, 'users/mobile/pw_reset_complete.html')


@login_required
@json_view
def password_change(request):
    """Change password form page."""
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return {'pw_change_complete': True}
    else:
        form = PasswordChangeForm(user=request.user)

    return jingo.render(request, 'users/desktop/pw_change.html', {'form': form})


@login_required
def password_change_complete(request):
    """Change password complete page."""
    return jingo.render(request, 'users/desktop/pw_change_complete.html')


@login_required
def delete_account(request):
    pass # TODO implement


def _clean_next_url(request):
    if 'next' in request.POST:
        url = request.POST.get('next')
    elif 'next' in request.GET:
        url = request.GET.get('next')
    else:
        url = request.META.get('HTTP_REFERER')

    if url:
        parsed_url = urlparse.urlparse(url)
        # Don't redirect outside of Spark.
        # Don't include protocol+domain, so if we are https we stay that way.
        if parsed_url.scheme:
            site_domain = Site.objects.get_current().domain
            url_domain = parsed_url.netloc
            if site_domain != url_domain:
                url = None
            else:
                url = u'?'.join([getattr(parsed_url, x) for x in
                                ('path', 'query') if getattr(parsed_url, x)])

        # Don't redirect right back to login or logout page
        if parsed_url.path in [settings.LOGIN_URL, settings.LOGOUT_URL]:
            url = None

    return url
