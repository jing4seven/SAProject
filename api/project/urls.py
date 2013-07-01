from django.conf.urls import patterns, url

from .views import projects_view, project_view, project_status_list_view, project_status_detail_view

urlpatterns = patterns('',
    url(r'^(?i)projects/$', projects_view.as_view(), name="all_projects_list_view"),
    url(r'^(?i)projects/(?P<owner_id>([0-9])+)/$', projects_view.as_view(), name="owner_projects_list_view"),         
    url(r'^(?i)project/(?P<pk>([0-9])+)/$', project_view.as_view(), name="project_view"),
    url(r'^(?i)project/(?P<project_id>([0-9])+)/project-status/$', project_status_list_view.as_view(), name="project_of_project_status_list_view"),
    url(r'^(?i)project-status/(?P<pk>([0-9])+)/$', project_status_detail_view.as_view(), name="project_status_view"),
)