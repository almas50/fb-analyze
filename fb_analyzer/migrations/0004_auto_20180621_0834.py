# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-21 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_analyzer', '0003_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='author',
            field=models.CharField(default='Null', max_length=200),
        ),
        migrations.AddField(
            model_name='result',
            name='data',
            field=models.TextField(default='Null'),
        ),
    ]
