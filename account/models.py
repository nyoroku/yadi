from __future__ import unicode_literals
from datetime import datetime, timedelta
from datetime import date
from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.dispatch import receiver
from django.db.models.signals import post_save
from gari.models import User
from django_countries.fields import CountryField
from django.core.urlresolvers import reverse


class Profile(models.Model):
    GENDER_CHOICES = (('female', 'Female'),
                      ('male', 'Male'),
                      )
    LOOKING_CHOICES = (('woman', 'Woman'),
                       ('man', 'Man'),
                       )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = ProcessedImageField(upload_to='latest', processors=[ResizeToFill(539, 303)],
                                format='JPEG',
                                options={'quality': 100}, blank=True, verbose_name='Profile Picture')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='female')
    look_for = models.CharField(max_length=10, choices=LOOKING_CHOICES, default='woman',
                                verbose_name='Looking for a'

                                )
    about_me = models.TextField(max_length=500, blank=True, verbose_name='About Me')
    looking_for_in_partner = models.TextField(max_length=500, blank=True,
                                              verbose_name='What are you looking for in a partner')
    country = CountryField(blank_label='(select_country)', blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    ##def save(self, *args, **kwargs):
        ##if not self.age:
          ##  self.age = ((datetime.now().date()-self.date_of_birth).days/365.25)
           ## super(Profile, self).save(*args, **kwargs)

    #def save(self, *args, **kwargs):
        #days_in_year = 365.2425
        #self.age = int((date.today() - self.date_of_birth).days / days_in_year)
        #super(Profile, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.date_of_birth = str(self.date_of_birth)
        if self.date_of_birth is not False:
            self.age = (
                       datetime.today().date() - datetime.strptime(self.date_of_birth, '%Y-%m-%d').date()) // timedelta(
                days=365)
            super(Profile, self).save(*args, **kwargs)



    def get_absolute_url(self):
        return reverse('member_detail', args=[self.id])




class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set')
    user_to = models.ForeignKey(User, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} likes {}'.format(self.user_from, self.user_to)

User.add_to_class('liking', models.ManyToManyField('self', through=Contact,
                                                   related_name='likers', symmetrical=False))









