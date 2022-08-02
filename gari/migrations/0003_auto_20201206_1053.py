# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2020-12-06 07:53
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('gari', '0002_auto_20201206_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='model',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='make', chained_model_field='make', on_delete=django.db.models.deletion.CASCADE, to='gari.Model'),
        ),
    ]