from django.conf.urls import patterns, url
from api.auth import views

urlpatterns = patterns('', 
	url(r'^(?i)(?P<owner_username>[a-z|0-9|_]{5,50})/(?P<project_name>[a-z|0-9|-]{5,50})/siteclients/$', \
		views.site_clients.as_view(), name="site_clients"),
	url(r'^(?i)(?P<owner_username>[a-z|0-9|_]{5,50})/(?P<project_name>[a-z|0-9|-]{5,50})/siteclient/(?P<pk>[0-9]+)/$', \
		views.site_client.as_view(), name="site_client"),
)