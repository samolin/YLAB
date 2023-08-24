import time

from .worker import celery


@celery.task
def db_sync():
    for i in range(10):
        time.sleep(5)
    return True
