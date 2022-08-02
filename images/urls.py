from django.conf.urls import url
from . import views

app_name = 'images'
urlpatterns = [

            url(r'^image_upload/$', views.upload_image, name='image_upload'),
            url(r'^image/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.image_detail, name='detail'),
            url(r'^my_images/$', views.my_images, name='my_images'),
]
