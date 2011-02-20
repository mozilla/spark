from django.contrib import auth
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm
from users.forms import RegisterForm
from users.models import Profile


def handle_login(request):
    if request.method == 'POST':
        auth.logout(request)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

        return form

    request.session.set_test_cookie()
    return AuthenticationForm()


def handle_register(request):
    """Handle to help registration."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            Profile.objects.create(user=new_user)
        return form
    return RegisterForm()
