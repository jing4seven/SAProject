from django.conf.urls import patterns, include, url
from frontend.secure import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SAProject.views.home', name='home'),
	url(r'(?i)user/$', views.dashboard_view.as_view(), name="user_view"),
)
