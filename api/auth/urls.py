from django.conf.urls import patterns, url
from api.auth import views

urlpatterns = patterns('', 
	url(r'^SiteClient/$', views.SiteClient.as_view(), name="SiteClient"),
	url(r'^SiteClient/(?P<pk>[0-9]+)/$', views.SiteClient.as_view(), name="SiteClient"),
)