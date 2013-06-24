from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SAProject.views.home', name='home'),
    url(r'^(?i)api-auth/', include('api.auth.urls')), 
    url(r'^(?i)user/', include('api.secure.urls')),
)