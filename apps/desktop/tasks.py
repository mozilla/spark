
from celery.decorators import task

@task
def a_test_task(some_data):
    test = 'foobar'