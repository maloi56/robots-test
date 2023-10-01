import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'R4C.settings')

app = Celery('R4C')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
CELERY_IMPORTS = ('users.signals', 'robots.signals',)
