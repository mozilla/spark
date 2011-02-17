from spark import decorators

def login_required(func):
    return decorators.login_required(func, mobile=True)

def logout_required(func):
    return decorators.logout_required(func, mobile=True)