import os
import urlparse
import json

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, 
                         Http404)
from django.views.decorators.http import require_http_methods, require_GET
from django.shortcuts import get_object_or_404
from django.utils.http import base36_to_int

import jingo

from spark.urlresolvers import reverse, clean_next_url
from spark.helpers import url
from spark.utils import is_mobile
from spark.decorators import (ssl_required, logout_required, login_required, 
                              post_required, json_view, ajax_required)

from users.backends import Sha256Backend
from users.forms import (EmailConfirmationForm, EmailChangeForm, PasswordResetForm,
                         PasswordChangeForm, PasswordConfirmationForm, SetPasswordForm)
from users.models import Profile
from users.utils import handle_login, handle_register

from responsys import responsys_async as responsys



@ssl_required
@json_view
def login(request, mobile=False):
    """Try to log the user in."""
    form = handle_login(request)
    
    next = clean_next_url(request)
    
    if mobile:
        next_url = next or reverse('mobile.home')
        
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
                        'next': next or reverse('desktop.home')}

        return HttpResponseBadRequest()


@ssl_required
def logout(request, mobile=False):
    """Log the user out."""
    auth.logout(request)
    next_url = clean_next_url(request) if 'next' in request.GET else ''
    home_view = 'mobile.home' if mobile else 'desktop.home'
    return HttpResponseRedirect(next_url or reverse(home_view))


@ssl_required
@logout_required
@require_http_methods(['GET', 'POST'])
def register(request):
    """Register a new user."""
    form = handle_register(request)
    if form.is_valid():
        # User is logged-in automatically after registration
        new_user = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password'])
        auth.login(request, new_user)
        
        # Register for newletters
        data = form.cleaned_data
        optins = []
        if data['newsletter']:
            optins.append(settings.MOZILLA_CAMPAIGN)
        if data['spark_newsletter']:
            optins.append(settings.SPARK_CAMPAIGN)
        
        if len(optins) > 0:
            # This will be async if Celery is enabled
            status= responsys.subscribe(optins,
                                        data['email'],
                                        'html',
                                        responsys.make_source_url(request),
                                        request.locale)
        
        # Set a flag for mobile menu notifications
        profile = User.objects.get(username=form.cleaned_data['username']).profile
        profile.new_challenges = True
        profile.save()
        
        return HttpResponseRedirect(reverse('mobile.home'))
    return jingo.render(request, 'users/mobile/register.html',
                        {'form': form})


@login_required
@post_required
@ajax_required
@json_view
def change_email(request):
    """Change email ajax view."""
    form = EmailChangeForm(request.user, request.POST)
    if not form.is_valid():
        return {'status': 'error',
                'errors': dict(form.errors.iteritems())}
    else:
        request.user.email = form.cleaned_data['new_email']
        request.user.save()
        return {'status': 'success'}


@login_required
@post_required
@ajax_required
@json_view
def password_change(request):
    """Change password ajax view."""
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if not form.is_valid():
        return {'status': 'error',
                'errors': dict(form.errors.iteritems())}
    else:
        form.save()
        return {'status': 'success'}


@login_required
@post_required
@ajax_required
@json_view
def delete_account(request):
    """Delete account ajax view."""
    form = PasswordConfirmationForm(user=request.user, data=request.POST)
    if not form.is_valid():
        return {'status': 'error',
                'errors': dict(form.errors.iteritems())}
    else:
        # Anonymize user instead of actually deleting it.
        # We need to keep user metadata in Profile and UserNode
        # so that the game keeps working as intended.
        # If we used user.delete() these would get deleted too.
        request.user.username = None
        request.user.password = None
        request.user.email = None
        request.user.is_active = False
        request.user.save()
        auth.logout(request)
        return {'status': 'success',
                'next': reverse('desktop.home')}


@json_view
def forgot_password(request, mobile=False):
    """Password reset form. This view sends an email with a reset link.
    """
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        valid = form.is_valid()
        if valid:
            form.save(use_https=request.is_secure(),
                      token_generator=default_token_generator,
                      email_template_name='users/email/pw_reset.ltxt')
        if mobile:
            if valid:
                return HttpResponseRedirect(reverse('users.mobile_pw_reset_sent'))
        else:
            if not valid:
                return {'status': 'error',
                        'errors': dict(form.errors.iteritems())}
            else:
                return {'status': 'success'}
    else:
        form = PasswordResetForm()

    if mobile:
        return jingo.render(request, 'users/mobile/pw_reset_form.html', {'form': form})


def password_reset_sent(request):
    """ Password reset email sent. This view shows a success message after
        email is sent.
    """
    return jingo.render(request, 'users/mobile/pw_reset_sent.html')


@ssl_required
@json_view
def password_reset_confirm(request, uidb36=None, token=None):
    """View that checks the hash in a password reset link and presents a
    form for entering a new password.
    
    It's used on both desktop (ajax) and mobile websites.
    """
    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404
    
    user = get_object_or_404(User, id=uid_int)
    context = {}
    
    # Display mobile or desktop version by sniffing user-agent
    mobile = is_mobile(request)

    if default_token_generator.check_token(user, token):
        context['validlink'] = True
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                if mobile:
                    return HttpResponseRedirect(reverse('users.mobile_pw_reset_complete'))
                else:
                    return {'status': 'success'}
            elif not mobile:
                    return {'status': 'error',
                            'errors': dict(form.errors.iteritems())}
        else:
            form = SetPasswordForm(None)
    else:
        context['validlink'] = False
        form = None
    context['form'] = form

    if mobile:
        return jingo.render(request, 'users/mobile/pw_reset_confirm.html', context)
    else:
        context.update({'uidb36': uidb36,
                        'token': token,
                        'is_pwreset': True,
                        'is_homepage': True})
        return jingo.render(request, 'desktop/home.html', context)


def password_reset_complete(request):
    """Password reset complete.
    """
    return jingo.render(request, 'users/mobile/pw_reset_complete.html')

