from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Buse (models.Model):
    reg = models.CharField(max_length=20, unique=True, verbose_name='Number Plate')
    name = models.CharField(max_length=20, unique=True, blank=True)
    date_added = models.DateField(verbose_name='Added On')

    def __unicode__(self):
        return unicode(self.reg)
    