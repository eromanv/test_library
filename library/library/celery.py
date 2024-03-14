from __future__ import absolute_import, unicode_literals
import os
import time
from django.conf import settings
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library.settings")


app = Celery("library")

app.config_from_object("django.conf:settings")
app.autodiscover_tasks()


@app.task()
def create_event_with_delay(event_id):
    from communication.models import Event
    time.sleep(10)
    print('time wait activate')
    event = Event.objects.get(pk=event_id)
    