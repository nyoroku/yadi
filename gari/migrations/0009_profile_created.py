# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2021-01-17 17:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gari', '0008_profile_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]