from django.conf.urls import patterns, url

from .views import projects_view, project_view, project_status_list_view, project_status_detail_view, \
                   releases_view, release_view, release_status_list_view, release_status_detail_view, \
                   work_item_groups_view, work_item_group_view, work_items_by_group_view, work_items_by_release_view, \
                   work_item_view
                   


urlpatterns = patterns('',
    # url(r'^(?i)projects/$', projects_view.as_view(), name="all_projects_list_view"),
    url(r'^(?i)owner/(?P<owner_username>([a-zA-Z]|[0-9]|\-|\_)+)/projects/$', projects_view.as_view(), name="owner_projects_list_view"),         
    url(r'^(?i)owner/(?P<owner_username>([a-zA-Z]|[0-9]|\-|\_)+)/project/(?P<project_name>([a-zA-Z]|[0-9]|\-|\_)+)/releases/$', releases_view.as_view(), name="project_releases_list_view"),

    # url(r'^(?i)project/(?P<project_id>([0-9])+)/$', project_view.as_view(), name="project_view"),
    # url(r'^(?i)project/(?P<project_id>([0-9])+)/project-status/$', project_status_list_view.as_view(), name="project_of_project_status_list_view"),
    # url(r'^(?i)project-status/(?P<project_status_id>([0-9])+)/$', project_status_detail_view.as_view(), name="project_status_view"),    
    # url(r'^(?i)project/(?P<project_id>([0-9])+)/releases/$', releases_view.as_view(), name="project_release_list_view"),
    # url(r'^(?i)release/(?P<release_id>([0-9])+)/$', release_view.as_view(), name="release_view"),
    # url(r'^(?i)release/(?P<release_id>([0-9])+)/release-status$', release_status_list_view.as_view(), name="release_status_list_view"),
    # url(r'^(?i)release-status/(?P<release_status_id>([0-9])+)/$', release_status_detail_view.as_view(), name="release_status_detail_view"),
    # url(r'^(?i)project/(?P<project_id>([0-9])+)/work-item-groups/$', work_item_groups_view.as_view(), name="project_work_item_groups_view"),
    # url(r'^(?i)work-item-group/(?P<work_item_group_id>([0-9])+)/$', work_item_group_view.as_view(), name="work_item_group_view"),
    # url(r'^(?i)work-item-group/(?P<work_item_group_id>([0-9])+)/work-items$', work_items_by_group_view.as_view(), name="work_items_by_group_view"),
    # url(r'^(?i)release/(?P<release_id>([0-9])+)/work-items$', work_items_by_release_view.as_view(), name="work_items_by_release_view"),
    # url(r'^(?i)work-item/(?P<work_item_id>([0-9])+)/$', work_item_view.as_view(), name="work_item_view"),
    
)