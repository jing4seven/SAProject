from django.conf.urls import patterns, url
from api.auth import views

urlpatterns = patterns('', 
	url(r'^(?i)siteclient/$', views.site_client.as_view(), name="site_client"),
	url(r'^(?i)siteclient/(?P<pk>[0-9]+)/$', views.site_client.as_view(), name="site_client"),
)