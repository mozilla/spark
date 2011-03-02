from django.contrib import auth
from django.contrib.auth.models import User

from mptt.exceptions import InvalidMove

from users.forms import RegisterForm, AuthenticationForm
from users.models import Profile, UserNode


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


def user_node(user):
    """Retrieves or creates a node in the user tree for this user."""
    try:
        user_node = user.node
    except UserNode.DoesNotExist:
        user_node = UserNode(user=user)
        user_node.save()
    
    return user_node


def create_relationship(parent, child):
    """Creates a parent-child relationship between two users."""
    child_node = user_node(child)
    parent_node = user_node(parent)
    
    if user_node and parent_node:
        try:
            child_node.parent = parent_node
            child_node.save()
            return True
        except InvalidMove:
            pass
    
    return False


def is_direct_child_of(user, parent):
    """Returns whether `user` is the direct child of `parent` in the user tree."""
    try:
        parent_node = UserNode.objects.get(user=parent)
        for child in parent_node.get_children():
            if child.user == user:
                return True
    except UserNode.DoesNotExist:
        pass
    
    return False


def is_part_of_chain_started_by(user, parent):
    """Returns whether `user` is part of a sharing chain started by `parent` in the user tree."""
    try:
        parent_node = UserNode.objects.get(user=parent)
        for descendant in parent_node.get_descendants():
            if descendant.user == user:
                return True
    except UserNode.DoesNotExist:
        pass
    
    return False


