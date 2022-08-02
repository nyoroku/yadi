from django.contrib import admin
from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ['caption', 'slug', 'picture', 'created']
    list_filter = ['created']


admin.site.register(Image, ImageAdmin)
