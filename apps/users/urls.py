from django.conf.urls.defaults import patterns, url, include

from spark.views import redirect_to
from users import views


desktop_patterns = patterns('',
    #  Login/logout (ajax)
    url(r'^login$', views.login, name='users.login'),
    url(r'^logout$', views.logout, name='users.logout'),
    
    # Forgot password (ajax)
    url(r'^forgotinfo$', views.forgot_password, name='users.forgot_password'),
    
    # Change password (ajax)
    url(r'^pwchange$', views.password_change, name='users.pw_change'),

    # Change email (ajax)
    url(r'^change_email$', views.change_email, name='users.change_email'),

    # Delete account (ajax)
    url(r'^delaccount$', views.delete_account, name='users.delete_account'),
)

opts = {'mobile': True}
mobile_patterns = patterns('',
    url(r'^login$', views.login, opts, name='users.mobile_login'),
    url(r'^logout$', views.logout, opts, name='users.mobile_logout'),
    
    # Sign up
    url(r'^register$', views.register, name='users.mobile_register'),
    
    # Forgot password
    url(r'^forgotinfo$', views.forgot_password, opts,
                                        name='users.mobile_forgot_password'),

    # Password reset
    url(r'^pwresetsent$', views.password_reset_sent, 
                                        name='users.mobile_pw_reset_sent'),
    url(r'^pwresetcomplete$', views.password_reset_complete,
                                        name="users.mobile_pw_reset_complete"),
)

urlpatterns = patterns('',
    # Password reset (handles both the mobile page and the ajax desktop popup)
    url(r'^pwreset/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)$',
        views.password_reset_confirm, name="users.pw_reset_confirm"),
        
    url(r'^users/', include(desktop_patterns)),
    url(r'^m/', include(mobile_patterns)),
)