from django.conf.urls import patterns, url
from api.secure import views

urlpatterns = patterns('', 
	url(r'^(?i)$', views.user_view.as_view(), name="user_view"),
	url(r'^(?i)(?P<username>[\w+]+)/$', views.user_view.as_view(), name="user_view"),
)