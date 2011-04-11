from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site

from users.models import User
from sharing.utils import url2qr

from .utils import render_to_pdf

def userposter(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    profile = user.profile
    base_url = u'https://%s' % Site.objects.get_current()
    
    print base_url
    
    return render_to_pdf(request,
            'poster/poster.html',
            {
                'base_url': base_url,
                'username': user.username,
                'user_url': profile.generic_sharing_url.replace('https://',''),
                'user_qr': profile.qr_code_download,
                'ff_home_qr': url2qr('http://www.mozilla.com/mobile/home/')
            }
        )