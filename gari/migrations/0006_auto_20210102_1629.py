# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2021-01-02 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gari', '0005_auto_20210102_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='door',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='engine_size',
            field=models.DecimalField(decimal_places=1, default=1.0, max_digits=3),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='fuel_type',
            field=models.CharField(choices=[('bi fuel', 'Bi Fuel'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('hybrid', 'Hybrid'), ('petrol', 'Petrol')], default='petrol', max_length=100),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='seat',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
