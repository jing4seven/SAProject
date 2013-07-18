from django.conf.urls import patterns, url
from api.auth import views

urlpatterns = patterns('',
    url(r'^(?i)site-clients/$', views.site_clients_view.as_view(), name="site_clients"),
    url(r'^(?i)site-client/(?P<pk>\d+)/$', views.site_client_view.as_view(), name="site_client"),
)
