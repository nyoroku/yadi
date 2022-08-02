"""Basika URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from gari.views import gari_pad
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', gari_pad, name='index'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^amazontech/', include('amazon.urls')),
    url(r'^gari/', include('gari.urls')),
    url(r'^compare/', include('compare.urls')),
    url(r'^trucks/', include('trucks.urls')),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^accounts/user/login/$', auth_views.login, {'template_name': 'user_login.html'},
                      name='user_login'),
    url(r'^accounts/user/logout/$', auth_views.logout, {'template_name': 'user_logged_out.html'},
                      name='user_logout'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^chaining/', include('smart_selects.urls')),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
