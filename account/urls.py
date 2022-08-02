from django.conf.urls import url
from . import views

app_name = 'account'
urlpatterns = [
          #url(r'^login/$', views.user_login, name='login')
          #url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
          url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logged_out.html', }, name='logout'),
          url(r'^logout-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),
          url(r'^$', views.profile, name='profile'),
          url(r'^password-change/$', 'django.contrib.auth.views.password_change', name='password_change'),
          url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
          url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
          url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
          url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)$',
              'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
          url(r'^password-reset/complete/$', 'django.contrib.auth.views.password_reset_complete',
              name='password_reset_complete'),
          url(r'^register/$', views.register, name='register'),
          url(r'^edit/$', views.edit, name='edit'),
          #url(r'^user_like/$', views.user_like, name='user_like'),
          url(r'^members/$', views.member_list, name='home'),
          url(r'^members/(?P<username>[-\w]+)/$', views.member_detail, name='member_detail'),
          url(r'^search/$', views.member_filter, name='search'),
          url(r'^matches/$', views.member_results, name='match'),









        ]
