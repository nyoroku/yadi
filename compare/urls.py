from django.conf.urls import url
from . import views
app_name = 'compare'
urlpatterns = [

 url(r'^$', views.compare_detail, name='compare_detail'),
 url(r'^add/(?P<vehicle_id>\d+)/$', views.compare_add, name='compare_add'),
 url(r'^remove/(?P<vehicle_id>\d+)/$', views.compare_remove, name='compare_remove'),

]