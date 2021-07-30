from __future__ import absolute_import
import os
from celery import Celery
from django.db import transaction
from celery.decorators import task
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fb_analyze.settings')
app = Celery('fb_analyze')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()