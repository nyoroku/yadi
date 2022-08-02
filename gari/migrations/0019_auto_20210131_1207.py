# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2021-01-31 09:07
from __future__ import unicode_literals

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gari', '0018_auto_20210131_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='model',
            name='picture',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='models'),
        ),
    ]