from __future__ import absolute_import, unicode_literals
from manage import get_env

from celery import Celery

get_env()

app = Celery('inventory_management')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request}')

# celery -A inventory_management worker -l info --pool=solo
