# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-05 16:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_auto_20160905_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='workers',
            field=models.ManyToManyField(help_text='Members helping with this event', to=settings.AUTH_USER_MODEL),
        ),
    ]
