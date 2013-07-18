from django.conf.urls import patterns, url
from api.secure import views

urlpatterns = patterns('',
    url(r'^(?i)users/$', views.users_view.as_view(), name="users_view"),
    url(r'^(?i)user/(?P<username>([a-zA-Z|0-9|\-|\_|.|@]){5,30})/$', views.user_view.as_view(), name="user_view"),

    # url(r'^(?i)role/$', views.role_view.as_view(), name="role_view"),
    # url(r'^(?i)role/(?P<name>([a-zA-Z]|[0-9]|-|_)+)/$', views.role_view.as_view(), name="role_view"),
    # url(r'^(?i)permission/$', views.permission_view.as_view(), name="permission_view"),
    # url(r'^(?i)permission/(?P<name>[a-zA-Z]+)/$', views.permission_view.as_view(), name="permission_view"),
)
