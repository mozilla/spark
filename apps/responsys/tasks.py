
from celery.decorators import task

from . import responsys as _responsys


@task
def subscribe_task(campaign, address, format='html', source_url='', lang=''):
    return _responsys.subscribe(campaign, address, format, source_url, lang)