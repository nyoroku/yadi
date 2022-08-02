from django.contrib import admin
import datetime
from .models import Buse


class BuseAdmin(admin.ModelAdmin):
    list_display = ['reg', 'name', 'date_added']
    search_fields = ['reg', 'name' 'date_added']
    list_filter = ['reg', 'name', 'date_added']
admin.site.register(Buse, BuseAdmin)
