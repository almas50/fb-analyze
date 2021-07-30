from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task
from fb_analyzer.models import Result
from fb_analyzer import fb_scrap
import time


@task(name="user_id")
def user_id(user):
    fb_data = fb_scrap.main(user)
    Result.objects.create(data=fb_data, author=user)
