from celery import Celery

from app.core.config import settings

celery = Celery('celery', broker=str(settings.rabbit.RABBIT_URL))
