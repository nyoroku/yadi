from __future__ import unicode_literals
from datetime import datetime, timedelta
from datetime import date
from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from smart_selects.db_fields import ChainedForeignKey
from gari.models import User


class Make(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(blank=True)
    created = models.DateField(default=datetime.now)
    slug = models.SlugField(default='vehicle', max_length=200)
    description = models.TextField(default='A Good brand')

    def save(self, *args, **kwargs):
        super(Make, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(self.id)
            self.save()

    def get_absolute_url(self):
        return reverse('gari:make-detail', args=[self.created.year,
                                                    self.created.strftime('%m'),
                                                    self.created.strftime('%d'),
                                                    self.slug])

    def __str__(self):
        return self.name


class Model(models.Model):
    make = models.ForeignKey(Make)
    name = models.CharField(max_length=200)
    lower_price = models.PositiveIntegerField(default=10000)
    higher_price = models.PositiveIntegerField(default=10000)
    description = models.TextField(default='A superb model')
    picture = ProcessedImageField(blank=True, upload_to='models', processors=[ResizeToFill(639, 426)],
                                  format='JPEG',
                                  options={'quality': 100})
    slug = models.SlugField(max_length=200, default='model')
    created = models.DateField(default=datetime.now)

    def get_absolute_url(self):
        return reverse('gari:model-detail', args=[self.created.year,
                                                    self.created.strftime('%m'),
                                                    self.created.strftime('%d'),
                                                    self.slug])

    def __str__(self):
        return self.name


class County(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Feature(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Truck(models.Model):
    STATUS = (('used', 'Used'),
            ('new', 'New'),
            ('import', 'Import')

            )
    COLOR = (('red', 'Red'),
              ('blue', 'Blue'),
              ('black', 'Black')

              )
    GEARBOX = (('manual', 'Manual'),
             ('automatic', 'Automatic'),


             )

    FUELTYPE = (('bi fuel', 'Bi Fuel'),
                ('diesel', 'Diesel'),
                ('electric', 'Electric'),
                ('hybrid', 'Hybrid'),
                ('petrol', 'Petrol'),


                )
    name = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    status = models.CharField(max_length=100, choices=STATUS)
    make = models.ForeignKey(Make)
    model = ChainedForeignKey(
        Model,
        chained_field="make",
        chained_model_field="make",
        show_all=False,
        auto_choose=False,
        sort=True)
    county = models.ForeignKey(County)
    color = models.CharField(max_length=100, choices=COLOR)
    features = models.ManyToManyField(Feature)
    created = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=200)
    sponsored = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    tags = TaggableManager()
    description = models.TextField()
    picture = ProcessedImageField(upload_to='vehicles', processors=[ResizeToFill(639, 426)],
                                  format='JPEG',
                                  options={'quality': 100})
    seller = models.ForeignKey(User, related_name='%(class)s_related')
    availability = models.BooleanField(default=True)
    mileage = models.PositiveIntegerField()
    gearbox = models.CharField(max_length=100, choices=GEARBOX)

    door = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=100, choices=FUELTYPE)
    engine_size = models.DecimalField(max_digits=3, decimal_places=1)
    deal = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Truck, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.make) + "-" + str(self.id)
            self.save()

    def get_absolute_url(self):
        return reverse('trucks:truck-detail', args=[self.created.year,
                                                 self.created.strftime('%m'),
                                                 self.created.strftime('%d'),
                                                 self.slug])


class Image(models.Model):
    title = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='images', processors=[ResizeToFill(1000, 600)],
                                format='JPEG',
                                options={'quality': 100})
    vehicle = models.ForeignKey(Truck, related_name='images')

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.title
