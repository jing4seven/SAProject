from django.conf.urls import patterns, include, url
from frontend.secure import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SAProject.views.home', name='home'),
	#url(r'(?i)user/(?P<username>([a-zA-Z]|[0-9]|\-|\_)+)/$', views.dashboard_view.as_view(), name="user_view"),
    url(r'(?i)dashboard/$', views.dashboard_view.as_view(), name="dashboard_view"),
    
    url(r'(?i)(?P<username>([a-zA-Z]|[0-9]|\-|\_)+)/projects/$', views.project_tree_view.as_view(), name="projects_tree_view"),
    
)

