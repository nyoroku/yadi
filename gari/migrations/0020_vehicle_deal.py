# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2021-02-01 09:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gari', '0019_auto_20210131_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='deal',
            field=models.BooleanField(default=False),
        ),
    ]
