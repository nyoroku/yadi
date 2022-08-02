from django.conf.urls import url
from . import views
from .views import CountyAutocomplete


app_name = 'trucks'
urlpatterns = [


    url(r'^mine/$', views.ManageTruckListView.as_view(), name='my_list'),
    url(r'^create/$', views.TruckCreateView.as_view(), name='truck_add'),
    url(r'^(?P<pk>\d+)/edit/$', views.TruckUpdateView.as_view(), name='truck_edit'),
    url(r'^(?P<pk>\d+)/delete/$', views.TruckDeleteView.as_view(), name='delete_truck'),
    url(
        r'^county-autocomplete/$',
        CountyAutocomplete.as_view(),
        name='county-autocomplete',
    ),
    url(r'^(?P<pk>\d+)/image/$', views.TruckImageUpdateView.as_view(), name='truck_image_update'),
    url(r'^truck/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' 
           r'(?P<vehicle>[-\w]+)/$',
           views.truck_detail,
           name='truck-detail'),
]