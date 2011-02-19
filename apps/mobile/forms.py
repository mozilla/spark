from django import forms
from django.core.validators import validate_email

from tower import ugettext as _, ugettext_lazy as _lazy

from users.models import User


IDENTIFIER_REQUIRED = _lazy(u'Please enter a username or email address.')
IDENTIFIER_NOTFOUND = _lazy(u'The username or email address you entered was not found.')
IDENTIFIER_SELF = _lazy(u'Did you really send a Spark to yourself?')

class BoostStep2Form(forms.Form):
    """ This form requires that one of its two fields be filled :
    
        - an identifier (username or email address) of the user who shared Spark with them.
        or
        - a checkbox meaning that the user got a Spark on their own.
    """
    identifier = forms.CharField(required=False)
    from_website = forms.BooleanField(required=False)
    
    def __init__(self, user, *args, **kwargs):
        super(BoostStep2Form, self).__init__(*args, **kwargs)
        self.user = user
        self.parent_username = None

    def clean(self):
        found = False
        identifier = self.cleaned_data['identifier']
        from_website = self.cleaned_data['from_website']
        
        # One of both fields must be filled
        if not identifier and not from_website:
            self.identifier_error(IDENTIFIER_REQUIRED)
            return self.cleaned_data
        
        # A user cannot specify himself as his own parent user
        if (self.user.email == identifier) or (self.user.username == identifier):
            self.identifier_error(IDENTIFIER_SELF)
            return self.cleaned_data

        parent = self.find_parent_user(identifier)

        if not parent and not from_website:
            self.identifier_error(IDENTIFIER_NOTFOUND)
        elif parent:
            self.parent_username = parent[0].username
        
        return self.cleaned_data

    def find_parent_user(self, identifier):
        try:
            # Check if the user has entered an email address
            validate_email(identifier)
            
            parent = User.objects.filter(email=identifier)
        except forms.ValidationError:
            # This must be a username then. Check if it exists.
            parent = User.objects.filter(username=identifier)
        
        return parent

    def identifier_error(self, msg):
        self._errors['identifier'] = self.error_class([msg])
