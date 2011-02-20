import re

from django.contrib.auth.models import User
from django.forms import ValidationError

from nose.tools import eq_
from pyquery import PyQuery as pq

from users.forms import RegisterForm, EmailConfirmationForm, EmailChangeForm
from users.tests import TestCaseBase


class RegisterFormTestCase(TestCaseBase):
    pass #TODO


class EmailConfirmationFormTestCase(TestCaseBase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = User.objects.get(username='rrosario')
        assert self.user.is_active

    def test_correct_email(self):
        form = EmailConfirmationForm(self.user, data={'email': 'user118577@nowhere.com'})
        assert form.is_valid()

    def test_invalid_email_address(self):
        form = EmailConfirmationForm(self.user, data={'email': 'invalid@.email'})
        assert not form.is_valid()


class EmailChangeFormTestCase(TestCaseBase):
    fixtures = ['users.json']
    
    def setUp(self):
        self.user = User.objects.get(username='rrosario')
        assert self.user.is_active

    def test_correct_password(self):
        form = EmailChangeForm(self.user, data={'password': 'wrongpass',
                                                'new_email': 'new_email@example.com'})
        assert not form.is_valid()
        
    def test_invalid_email_address(self):
        form = EmailChangeForm(self.user, data={'password': 'testpass',
                                                'new_email': 'invalid@.email'})
        assert not form.is_valid()
        
