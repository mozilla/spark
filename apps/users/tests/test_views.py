from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core import mail

import mock
from nose.tools import eq_
from pyquery import PyQuery as pq

from spark.tests import TestCase, LocalizingClient
from spark.urlresolvers import reverse


class RegisterTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.old_debug = settings.DEBUG
        settings.DEBUG = True
        self.client.logout()

    def tearDown(self):
        settings.DEBUG = self.old_debug

    @mock.patch_object(Site.objects, 'get_current')
    def test_new_user(self, get_current):
        get_current.return_value.domain = 'su.mo.com'
        response = self.client.post(reverse('users.mobile_register', locale='en-US'),
                                    {'username': 'newbie',
                                     'email': 'newbie@example.com',
                                     'password': 'foobarbaz',
                                     'password2': 'foobarbaz'})
        eq_(302, response.status_code)
        u = User.objects.get(username='newbie')
        assert u.password.startswith('sha256')

        # Now try to log in
        u.save()
        response = self.client.post(reverse('users.mobile_login', locale='en-US'),
                                    {'username': 'newbie',
                                     'password': 'foobarbaz'}, follow=True)
        eq_(200, response.status_code)
        eq_('http://testserver/en-US/m/home', response.redirect_chain[0][0])

    @mock.patch_object(Site.objects, 'get_current')
    def test_unicode_password(self, get_current):
        u_str = u'\xe5\xe5\xee\xe9\xf8\xe7\u6709\u52b9'
        get_current.return_value.domain = 'su.mo.com'
        response = self.client.post(reverse('users.mobile_register', locale='en-US'),#locale='ja'),
                                    {'username': 'cjkuser',
                                     'email': 'cjkuser@example.com',
                                     'password': u_str,
                                     'password2': u_str}, follow=True)
        eq_(200, response.status_code)
        u = User.objects.get(username='cjkuser')
        u.save()
        assert u.password.startswith('sha256')

        # make sure you can login now
        response = self.client.post(reverse('users.mobile_login', locale='en-US'),#locale='ja'),
                                    {'username': 'cjkuser',
                                     'password': u_str}, follow=True)
        eq_(200, response.status_code)
        #eq_('http://testserver/ja/home', response.redirect_chain[0][0])
        eq_('http://testserver/en-US/m/home', response.redirect_chain[0][0])

    def test_duplicate_username(self):
        response = self.client.post(reverse('users.mobile_register', locale='en-US'),
                                    {'username': 'jsocol',
                                     'email': 'newbie@example.com',
                                     'password': 'foobarbaz',
                                     'password2': 'foobarbaz'}, follow=True)
        self.assertContains(response, "not right")

    def test_duplicate_email(self):
        User.objects.create(username='noob', email='noob@example.com').save()
        response = self.client.post(reverse('users.mobile_register', locale='en-US'),
                                    {'username': 'newbie',
                                     'email': 'noob@example.com',
                                     'password': 'foobarbaz',
                                     'password2': 'foobarbaz'}, follow=True)
        self.assertContains(response, "not right")


    def test_no_match_passwords(self):
        response = self.client.post(reverse('users.mobile_register', locale='en-US'),
                                    {'username': 'newbie',
                                     'email': 'newbie@example.com',
                                     'password': 'foobarbaz',
                                     'password2': 'barfoobaz'}, follow=True)
        self.assertContains(response, 'do not match')


class ChangeEmailTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = LocalizingClient()
        self.url = reverse('users.change_email')
                
    def test_user_change_email_same(self):
        """Changing to same email shows validation error."""
        self.client.login(username='rrosario', password='testpass')
        user = User.objects.get(username='rrosario')
        user.email = 'valid@email.com'
        user.save()
        response = self.client.post(self.url,
                                    {'password': 'testpass',
                                     'new_email': user.email})
        eq_(200, response.status_code)
        doc = pq(response.content)
        eq_('This is your current email address.', doc('ul.errorlist').text())

    def test_user_change_email_duplicate(self):
        """Changing to same email shows validation error."""
        self.client.login(username='rrosario', password='testpass')
        email = 'newvalid@email.com'
        User.objects.filter(username='pcraciunoiu').update(email=email)
        response = self.client.post(self.url,
                                    {'password': 'testpass',
                                     'new_email': email})
        eq_(200, response.status_code)
        doc = pq(response.content)
        eq_('A user with that email address already exists.',
            doc('ul.errorlist').text())

    def test_user_enters_wrong_password(self):
        """Entering wrong password shows validation error."""
        self.client.login(username='rrosario', password='testpass')
        user = User.objects.get(username='rrosario')
        user.email = 'valid@email.com'
        user.save()
        response = self.client.post(self.url,
                                    {'password': 'wrongpass',
                                     'new_email': 'new_email@example.com'})
        eq_(200, response.status_code)
        doc = pq(response.content)
        eq_('Please enter your current password.', doc('ul.errorlist').text())
        
