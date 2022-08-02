from django.conf.urls import url
from . import views
from .views import CountyAutocomplete, ModelAutocomplete, DealerCountyAutocomplete

app_name = 'gari'
urlpatterns = [

    url(r'^common/$', views.common_view, name='common'),
    url(r'^mine/$', views.ManageVehicleListView.as_view(), name='my_list'),
    url(r'^create/$', views.VehicleCreateView.as_view(), name='vehicle_add'),
    url(r'^(?P<pk>\d+)/edit/$', views.VehicleUpdateView.as_view(), name='vehicle_edit'),
    url(r'^(?P<pk>\d+)/delete/$', views.VehicleDeleteView.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/image/$', views.VehicleImageUpdateView.as_view(), name='vehicle_image_update'),
    url(r'^vehicle/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' 
           r'(?P<vehicle>[-\w]+)/$',
           views.vehicle_detail,
           name='vehicle-detail'),
    url(r'^dealer_register/$', views.DealerSignUpView.as_view(), name='dealer_registration'),
    url(r'^seller_register/$', views.PrivateSignUpView.as_view(), name='private_registration'),
    url(r'^profile_edit/$', views.edit, name='edit'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile-edit/$', views.edit_profile, name='edit_profile'),
    url(r'^my_profile/$', views.my_profile, name='my_profile'),
    url('ajax/load-models/', views.load_models, name='ajax_load_models'),
    url(
        r'^county-autocomplete/$',
        CountyAutocomplete.as_view(),
        name='county-autocomplete',
    ),
    url(
        r'^make-autocomplete/$',
        ModelAutocomplete.as_view(),
        name='make-autocomplete',
    ),
    url(
        r'^countydealer-autocomplete/$',
        DealerCountyAutocomplete.as_view(),
        name='countydealer-autocomplete',
    ),
    url(r'^gari-search/$', views.gari_pad, name='used_search'),
    url(r'^dealer-search/$', views.countyfilter, name='dealer_search'),
    url(r'^vehicle-search/$', views.gari_results, name='gari_results'),
    url(r'^allmakes/', views.all_makes, name='allbrands'),
    url(r'^allvehicles/', views.all_vehicles, name='allvehicles'),
    url(r'^alltypes/', views.all_type, name='alltypes'),
    url(r'^alldeals/', views.all_deals, name='alldeals'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.all_vehicles,
        name='allvehicle_by_tag'),
    url(r'^alldealers/', views.all_dealers, name='alldealers'),
    url(r'^profile/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' 
           r'(?P<profile>[-\w]+)/$',
           views.dealer_detail,
           name='dealer-detail'),
    url(r'^(?P<pk>\d+)/used/$', views.dealer_used, name='allused'),
    url(r'^(?P<pk>\d+)/new/$', views.dealer_new, name='allnew'),
    url(r'^(?P<pk>\d+)/imports/$', views.dealer_import, name='allimports'),
    url(r'^create-quote/$', views.create_quote, name='create_quote'),
    url(r'^all-quotes/$', views.all_quotes, name='all_quotes'),
    url(r'^my-quotes/$', views.my_quotes, name='my_quotes'),
    url(r'^make_offer/(?P<quote_id>\d+)/$', views.make_offer, name='make_offer'),
    url(r'^make/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' 
        r'(?P<make>[-\w]+)/$',
        views.make_detail,
        name='make-detail'),
    url(r'^type/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' 
        r'(?P<type>[-\w]+)/$',
        views.type_detail,
        name='type-detail'),
    url(r'^allnews/', views.allnews, name='allnews'),
    url(r'^tags/(?P<tag_slug>[-\w]+)/$', views.allnews,
          name='allnews_by_tag'),
    url(r'^new/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' 
           r'(?P<new>[-\w]+)/$',
           views.latest_detail,
           name='latest-detail'),
    url(r'^model/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' 
        r'(?P<model>[-\w]+)/$',
        views.model_detail,
        name='model-detail'),
]