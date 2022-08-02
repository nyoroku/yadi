from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.urlresolvers import reverse


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='members_image')
    caption = models.CharField(max_length=20, blank=True)
    slug = models.SlugField(max_length=20, blank=True)
    picture = ProcessedImageField(upload_to='pictures', processors=[ResizeToFill(300, 300)],
                                  format='JPEG',
                                  options={'quality': 100}, blank=True)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.caption

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.caption)
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])





