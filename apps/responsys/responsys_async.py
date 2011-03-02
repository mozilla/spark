""" Got Celery in Production? Use this driver
    for better throughput and a brighter smile. """

from celery.decorators import task

from . import responsys as _responsys

@task
def subscribe(campaign, address, format='html', source_url='', lang=''):
    """ Keep API in sync with responsys.py """
    return _responsys.subscribe(campaign, address, format, source_url, lang)

def make_source_url(request):
    """ Keep API in sync with responsys.py """
    return _responsys.make_source_url(request)
