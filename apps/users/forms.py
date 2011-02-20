import re

from django import forms
from django.conf import settings
from django.contrib.auth.models import User

from tower import ugettext as _, ugettext_lazy as _lazy

from users.models import Profile


USERNAME_INVALID = _lazy(u'Username may contain only letters, '
                         'numbers and @/./+/-/_ characters.')
USERNAME_REQUIRED = _lazy(u'Please enter a username.')
USERNAME_SHORT = _lazy(u'Username is too short (%(show_value)s characters). '
                       'It must be at least %(limit_value)s characters.')
USERNAME_LONG = _lazy(u'Username is too long (%(show_value)s characters). '
                      'It must be %(limit_value)s characters or less.')
EMAIL_INVALID = _lazy(u'Please enter a valid email address.')
PASSWD_REQUIRED = _lazy(u'Please enter a valid password.')
#PASSWD2_REQUIRED = _lazy(u'Please enter your password twice.')


class RegisterForm(forms.ModelForm):
    """A user registration form that detects duplicate email addresses.

    The default Django user creation form does not require email addresses
    to be unique. This form does, and sets a minimum length
    for usernames.
    """
    username = forms.RegexField(max_length=30, min_length=4,
        regex=r'^[\w.@+-]+$',
        error_messages={'invalid': USERNAME_INVALID,
                        'required': USERNAME_REQUIRED,
                        'min_length': USERNAME_SHORT,
                        'max_length': USERNAME_LONG})
    password = forms.CharField(error_messages={'required': PASSWD_REQUIRED})
    email = forms.EmailField(error_messages={'invalid': EMAIL_INVALID},
                             required=False)
#    password2 = forms.CharField(error_messages={'required': PASSWD2_REQUIRED})
    newsletter = forms.BooleanField(required=False)

    class Meta(object):
        model = User
        #fields = ('username', 'password', 'password2', 'email')
        fields = ('username', 'password', 'email')

    def clean(self):
        super(RegisterForm, self).clean()
        password = self.cleaned_data.get('password')
        #password2 = self.cleaned_data.get('password2')
        #if not password == password2:
        #    raise forms.ValidationError(_('Passwords must match.'))

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('A user with that email address '
                                          'already exists.'))
        return email

    def __init__(self,  request=None, *args, **kwargs):
        super(RegisterForm, self).__init__(request, auto_id='id_for_%s',
                                           *args, **kwargs)


class EmailConfirmationForm(forms.Form):
    """A simple form that requires an email address."""
    email = forms.EmailField(label=_lazy(u'Email address:'))


class EmailChangeForm(forms.Form):
    """A simple form that requires a password and an email address.
    
    It validates that it's the correct password for the current user and that it is not 
    the current user's email.
    """
    password = forms.CharField(label=_lazy(u"Password:"),
                    widget=forms.PasswordInput(render_value=False,
                                               attrs={'placeholder':_lazy(u'Password')}))
    new_email = forms.EmailField(label=_lazy(u'New email address:'),
                    widget=forms.TextInput(attrs={'placeholder':_lazy(u'Email address')}))

    def __init__(self, user, *args, **kwargs):
        super(EmailChangeForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_new_email(self):
        password = self.cleaned_data['password']
        new_email = self.cleaned_data['new_email']
        if not self.user.check_password(password):
            raise forms.ValidationError(_('Please enter a correct password.'))
        if self.user.email == new_email:
            raise forms.ValidationError(_('This is your current email.'))
        if User.objects.filter(email=new_email).exists():
            raise forms.ValidationError(_('A user with that email address '
                                          'already exists.'))
        return self.cleaned_data['new_email']

## TODO : PasswordChangeForm, PasswordConfirmation
