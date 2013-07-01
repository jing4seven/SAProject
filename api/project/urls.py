from django.conf.urls import patterns, url

from .views import projects_view, project_view

urlpatterns = patterns('',
    url(r'^(?i)projects/$', projects_view.as_view(), name="all_projects_list_view"),
    url(r'^(?i)projects/(?P<owner_id>([0-9])+)/$', projects_view.as_view(), name="owner_projects_list_view"),         
    url(r'^(?i)project/(?P<pk>([0-9])+)/$', project_view.as_view(), name="project_view"),
)