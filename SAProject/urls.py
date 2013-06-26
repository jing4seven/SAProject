from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SAProject.views.home', name='home'),
    url(r'^(?i)secure/', include('frontend.secure.urls')),

    url(r'^(?i)api/', include('api.auth.urls')),
    url(r'^(?i)api/secure/', include('api.secure.urls')),
)
