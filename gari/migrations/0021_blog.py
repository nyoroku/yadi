# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2021-02-01 15:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import smart_selects.db_fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('gari', '0020_vehicle_deal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('text', models.TextField()),
                ('writer', models.CharField(max_length=100)),
                ('picture', imagekit.models.fields.ProcessedImageField(upload_to='images')),
                ('make', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='gari.Make')),
                ('model', smart_selects.db_fields.ChainedForeignKey(chained_field='make', chained_model_field='make', on_delete=django.db.models.deletion.CASCADE, to='gari.Model')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]