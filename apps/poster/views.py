from django.shortcuts import get_object_or_404

from users.models import User
from sharing.utils import url2qr

from .utils import render_to_pdf

def userposter(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    profile = user.profile
    
    return render_to_pdf(request,
            'poster/poster.html',
            {
                'username': user.username,
                'user_url': profile.generic_sharing_url.replace('https://',''),
                'user_qr': profile.qr_code_download,
                'ff_home_qr': url2qr('http://www.mozilla.com/mobile/home/')
            }
        )