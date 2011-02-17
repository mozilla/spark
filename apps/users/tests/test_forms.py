import re

from django.contrib.auth.models import User
from django.forms import ValidationError

from nose.tools import eq_
from pyquery import PyQuery as pq

from users.forms import RegisterForm, EmailChangeForm
from users.tests import TestCaseBase


class RegisterFormTestCase(TestCaseBase):
    pass #TODO
    

class EmailChangeFormTestCase(TestCaseBase):
    fixtures = ['users.json']
    
    def test_correct_password(self):
        user = User.objects.get(username='rrosario')
        assert user.is_active
        form = EmailChangeForm(user, data={'password': 'wrongpass',
                                           'new_email': 'new_email@example.com'})
        assert not form.is_valid()