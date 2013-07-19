from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?i)secure/', include('frontend.secure.urls')),

    url(r'^(?i)api/auth/', include('api.auth.urls')),
    url(r'^(?i)api/secure/', include('api.secure.urls')),
    url(r'^(?i)api/', include('api.project.urls')),
)
