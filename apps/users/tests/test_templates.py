from copy import deepcopy
import hashlib
import os
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core import mail
from django.core.files import File
from django.utils.http import int_to_base36

import mock
from nose.tools import eq_
from pyquery import PyQuery as pq
from test_utils import RequestFactory

from spark.urlresolvers import reverse
from spark.helpers import urlparams

from spark.tests import post

from users.models import Profile
from users.tests import TestCaseBase


class LoginTests(TestCaseBase):
    """Login tests."""
    fixtures = ['users.json']

    def setUp(self):
        super(LoginTests, self).setUp()
        self.orig_debug = settings.DEBUG
        settings.DEBUG = True

    def tearDown(self):
        super(LoginTests, self).tearDown()
        settings.DEBUG = self.orig_debug

    def test_login_bad_password(self):
        '''Test login with a good username and bad password.'''
        response = post(self.client, 'users.login',
                        {'username': 'rrosario', 'password': 'foobar'})
        eq_(200, response.status_code)
        doc = pq(response.content)
        eq_('Please enter a correct username and password. Note that both '
            'fields are case-sensitive.', doc('ul.errorlist li').text())

    def test_login_bad_username(self):
        '''Test login with a bad username.'''
        response = post(self.client, 'users.login',
                        {'username': 'foobarbizbin', 'password': 'testpass'})
        eq_(200, response.status_code)
        doc = pq(response.content)
        eq_('Please enter a correct username and password. Note that both '
            'fields are case-sensitive.', doc('ul.errorlist li').text())

    def test_login(self):
        '''Test a valid login.'''
        response = self.client.post(reverse('users.login'),
                                    {'username': 'rrosario',
                                     'password': 'testpass'})
        eq_(302, response.status_code)
        eq_('http://testserver' +
                reverse('desktop.home', locale=settings.LANGUAGE_CODE),
            response['location'])

    def test_login_next_parameter(self):
        '''Test with a valid ?next=url parameter.'''
        next = '/kb/new'

        # Verify that next parameter is set in form hidden field.
        response = self.client.get(urlparams(reverse('users.login'),
                                             next=next))
        eq_(200, response.status_code)
        doc = pq(response.content)
        eq_(next, doc('input[name="next"]')[0].attrib['value'])

        # Verify that it gets used on form POST.
        response = self.client.post(reverse('users.login'),
                                    {'username': 'rrosario',
                                     'password': 'testpass',
                                     'next': next})
        eq_(302, response.status_code)
        eq_('http://testserver' + next, response['location'])

    @mock.patch_object(Site.objects, 'get_current')
    def test_login_invalid_next_parameter(self, get_current):
        '''Test with an invalid ?next=http://example.com parameter.'''
        get_current.return_value.domain = 'testserver.com'
        invalid_next = 'http://foobar.com/evil/'
        valid_next = reverse('desktop.home', locale=settings.LANGUAGE_CODE)

        # Verify that _valid_ next parameter is set in form hidden field.
        response = self.client.get(urlparams(reverse('users.login'),
                                             next=invalid_next))
        eq_(200, response.status_code)
        doc = pq(response.content)
        eq_(valid_next, doc('input[name="next"]')[0].attrib['value'])

        # Verify that it gets used on form POST.
        response = self.client.post(reverse('users.login'),
                                    {'username': 'rrosario',
                                     'password': 'testpass',
                                     'next': invalid_next})
        eq_(302, response.status_code)
        eq_('http://testserver' + valid_next, response['location'])

    def test_login_legacy_password(self):
        '''Test logging in with a legacy md5 password.'''
        legacypw = 'legacypass'

        # Set the user's password to an md5
        user = User.objects.get(username='rrosario')
        user.password = hashlib.md5(legacypw).hexdigest()
        user.save()

        # Log in and verify that it's updated to a SHA-256
        response = self.client.post(reverse('users.login'),
                                    {'username': 'rrosario',
                                     'password': legacypw})
        eq_(302, response.status_code)
        user = User.objects.get(username='rrosario')
        assert user.password.startswith('sha256$')

        # Try to log in again.
        response = self.client.post(reverse('users.login'),
                                    {'username': 'rrosario',
                                     'password': legacypw})
        eq_(302, response.status_code)


class PasswordReset(TestCaseBase):
    fixtures = ['users.json']

    def setUp(self):
        super(PasswordReset, self).setUp()
        self.user = User.objects.get(username='rrosario')
        self.user.email = 'valid@email.com'
        self.user.save()
        self.uidb36 = int_to_base36(self.user.id)
        self.token = default_token_generator.make_token(self.user)
        self.orig_debug = settings.DEBUG
        settings.DEBUG = True

    def tearDown(self):
        super(PasswordReset, self).tearDown()
        settings.DEBUG = self.orig_debug

    def test_bad_email_ajax(self):
        r = self.client.post(reverse('users.forgot_password'),
                             {'email': 'foo@bar.com'})
        eq_(200, r.status_code)
        eq_(True, json.loads(r.content)['pw_reset_sent'])
        eq_(0, len(mail.outbox))
    
    def test_bad_email_mobile(self):
        r = self.client.post(reverse('users.mobile_forgot_password'),
                             {'email': 'foo@bar.com'})
        eq_(302, r.status_code)
        eq_('http://testserver/en-US/m/pwresetsent', r['location'])
        eq_(0, len(mail.outbox))

    @mock.patch_object(Site.objects, 'get_current')
    def test_success(self, get_current):
        get_current.return_value.domain = 'testserver.com'
        r = self.client.post(reverse('users.mobile_forgot_password'),
                             {'email': self.user.email})
        eq_(302, r.status_code)
        eq_('http://testserver/en-US/m/pwresetsent', r['location'])
        eq_(1, len(mail.outbox))
        assert mail.outbox[0].subject.find('Password reset') == 0
        assert mail.outbox[0].body.find('pwreset/%s' % self.uidb36) > 0

    def _get_mobile_reset_url(self):
        return reverse('users.pw_reset_confirm',
                       args=[self.uidb36, self.token])

    def test_bad_reset_url(self):
        r = self.client.get('/m/pwreset/junk/', follow=True)
        eq_(r.status_code, 404)

        r = self.client.get(reverse('users.pw_reset_confirm',
                                    args=[self.uidb36, '12-345']))
        eq_(200, r.status_code)
        doc = pq(r.content)
        eq_('Password reset unsuccessful', doc('#header h1').text())

    def test_reset_fail(self):
        url = self._get_mobile_reset_url()
        r = self.client.post(url, {'new_password1': '', 'new_password2': ''})
        eq_(200, r.status_code)
        doc = pq(r.content)
        assert len(doc('ul.errorlist li')) > 0

        r = self.client.post(url, {'new_password1': 'one',
                                   'new_password2': 'two'})
        eq_(200, r.status_code)
        doc = pq(r.content)
        eq_("The two password fields didn't match.",
            doc('ul.errorlist li').text())

    def test_reset_success(self):
        url = self._get_mobile_reset_url()
        new_pw = 'fjdka387fvstrongpassword!'
        assert self.user.check_password(new_pw) is False

        r = self.client.post(url, {'new_password1': new_pw,
                               'new_password2': new_pw})
        eq_(302, r.status_code)
        eq_('http://testserver/en-US/m/pwresetcomplete', r['location'])
        self.user = User.objects.get(username='rrosario')
        assert self.user.check_password(new_pw)
        
    # TODO add missing ajax tests


class PasswordChangeTests(TestCaseBase):
    fixtures = ['users.json']

    def setUp(self):
        super(PasswordChangeTests, self).setUp()
        self.user = User.objects.get(username='rrosario')
        self.url = reverse('users.pw_change')
        self.new_pw = 'fjdka387fvstrongpassword!'
        self.client.login(username='rrosario', password='testpass')

    def test_change_password(self):
        assert self.user.check_password(self.new_pw) is False

        r = self.client.post(self.url, {'old_password': 'testpass',
                                        'new_password1': self.new_pw,
                                        'new_password2': self.new_pw})
        eq_(200, r.status_code)
        eq_(True, json.loads(r.content)['pw_change_complete'])
        self.user = User.objects.get(username='rrosario')
        assert self.user.check_password(self.new_pw)

    def test_bad_old_password(self):
        r = self.client.post(self.url, {'old_password': 'testpqss',
                                        'new_password1': self.new_pw,
                                        'new_password2': self.new_pw})
        eq_(200, r.status_code)
        doc = pq(r.content)
        eq_('Your old password was entered incorrectly. Please enter it '
            'again.', doc('ul.errorlist').text())

    def test_new_pw_doesnt_match(self):
        r = self.client.post(self.url, {'old_password': 'testpqss',
                                        'new_password1': self.new_pw,
                                        'new_password2': self.new_pw + '1'})
        eq_(200, r.status_code)
        doc = pq(r.content)
        eq_("Your old password was entered incorrectly. Please enter it "
            "again. The two password fields didn't match.",
            doc('ul.errorlist').text())

class EmailChangeTests(TestCaseBase):
    fixtures = ['users.json']
    
    def setUp(self):
        super(EmailChangeTests, self).setUp()
        self.url = reverse('users.change_email')
        self.user = User.objects.get(username='rrosario')
        self.client.login(username='rrosario', password='testpass')

    def test_display_current_email(self):
        """Page should display the user's current email."""
        r = self.client.get(self.url)
        eq_(200, r.status_code)
        doc = pq(r.content)
        eq_("user118577@nowhere.com", doc('#email').text())
