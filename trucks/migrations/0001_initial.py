# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2021-02-27 10:34
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import smart_selects.db_fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='images')),
            ],
            options={
                'ordering': ('-date_added',),
            },
        ),
        migrations.CreateModel(
            name='Make',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('logo', models.ImageField(blank=True, upload_to=b'')),
                ('created', models.DateField(default=datetime.datetime.now)),
                ('slug', models.SlugField(default='vehicle', max_length=200)),
                ('description', models.TextField(default='A Good brand')),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('lower_price', models.PositiveIntegerField(default=10000)),
                ('higher_price', models.PositiveIntegerField(default=10000)),
                ('description', models.TextField(default='A superb model')),
                ('picture', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='models')),
                ('slug', models.SlugField(default='model', max_length=200)),
                ('created', models.DateField(default=datetime.datetime.now)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trucks.Make')),
            ],
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('year', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('used', 'Used'), ('new', 'New'), ('import', 'Import')], max_length=100)),
                ('color', models.CharField(choices=[('red', 'Red'), ('blue', 'Blue'), ('black', 'Black')], max_length=100)),
                ('created', models.DateField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=200)),
                ('sponsored', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('picture', imagekit.models.fields.ProcessedImageField(upload_to='vehicles')),
                ('availability', models.BooleanField(default=True)),
                ('mileage', models.PositiveIntegerField()),
                ('gearbox', models.CharField(choices=[('manual', 'Manual'), ('automatic', 'Automatic')], max_length=100)),
                ('door', models.PositiveIntegerField()),
                ('seat', models.PositiveIntegerField()),
                ('fuel_type', models.CharField(choices=[('bi fuel', 'Bi Fuel'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('hybrid', 'Hybrid'), ('petrol', 'Petrol')], max_length=100)),
                ('engine_size', models.DecimalField(decimal_places=1, max_digits=3)),
                ('deal', models.BooleanField(default=False)),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trucks.County')),
                ('features', models.ManyToManyField(to='trucks.Feature')),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trucks.Make')),
                ('model', smart_selects.db_fields.ChainedForeignKey(chained_field='make', chained_model_field='make', on_delete=django.db.models.deletion.CASCADE, to='trucks.Model')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='truck_related', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='trucks.Truck'),
        ),
    ]
