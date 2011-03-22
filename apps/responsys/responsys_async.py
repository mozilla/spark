
from django.conf import settings

from . import responsys as _responsys
from .tasks import subscribe_task


def make_source_url(request):
    """ Keep API in sync with responsys.py """
    return _responsys.make_source_url(request)

def subscribe(campaigns, address, format='html', source_url='', lang=''):
    """ Keep API in sync with responsys.py """
    try:
        if settings.CELERY_ENABLED:
            subscribe_task.delay(campaigns, address, format, source_url, lang)
            return True
    except AttributeError:
        return False