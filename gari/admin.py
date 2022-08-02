from django.contrib import admin
from .models import Vehicle, County, Make, Model, Profile, Private, User, Feature, Service, Quote, Blog, Type


class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
    list_filter = ['username']
admin.site.register(User, UserAdmin)


class DealerAdmin(admin.ModelAdmin):
    list_display = ['company']
    list_filter = ['company']


admin.site.register(Profile, DealerAdmin)


class PrivateAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['user']


admin.site.register(Private, PrivateAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']


admin.site.register(Vehicle, VehicleAdmin)


class CountyAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']


admin.site.register(County, CountyAdmin)


class ModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']


admin.site.register(Model, ModelAdmin)


class MakeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']


admin.site.register(Make, MakeAdmin)


class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']


admin.site.register(Feature, FeatureAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']


admin.site.register(Service, ServiceAdmin)


class QuoteAdmin(admin.ModelAdmin):
    list_display = ['make']
    list_filter = ['make']


admin.site.register(Quote, QuoteAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']


admin.site.register(Blog, BlogAdmin)


class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']


admin.site.register(Type, TypeAdmin)
