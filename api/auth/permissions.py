from django.http import Http404
from django.conf import settings
from rest_framework import  permissions
from api.secure.models import project_user_role
from api.secure.models import user, role
from api.project.models import project

class api_permission(permissions.BasePermission):
    '''
    A implement class that match site client permission to socpes.
    '''
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.

        All we need to do here is that:
        We need get a set of permission for current user, if it's super user, just
        return True.

        For PRIVATE project, only project members can view (GET method), instead of
        Anonymous, so we should check if current user is a team member before next
        step.
        """

        #ToDo:
        # 1. How to get view's namespace here?                  DONE
        # 2. How to get project_name and owner_username here?     DONE
        # 3. How to enable session data here?

        # ToDo: Apply session on permission checking.

        # super user has all permissions.
        if request.user.is_superuser:
            return True

        # check if project is PRIVATE
        project_is_private = False
        perm_parm_dict = {'owner_username':'', 'project_name':''}
        perm_parm_dict.update(request.__dict__['parser_context']['kwargs'])

        owner_username = perm_parm_dict['owner_username']
        project_name = perm_parm_dict['project_name']

        perm_list = []
        if project_name and owner_username:
            proj_ins = self.__get_project_instance(owner_username, project_name)
            project_is_private = self.__check_project_private(proj_ins)
            if project_is_private and not self.__is_team_member(proj_ins, request.user):
                # check if current user is team member.
                return False
            perm_list = proj_ins.get_permissions_by_username(request.user)

        if not len(perm_list):
            perm_list = self.__get_anonymous_permissions()

        # get view namespace
        view_namespace = self.__get_fullname(view)

        return self.__has_permission_on_view(request.method, view_namespace, perm_list)

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def __has_permission_on_view(method, view_namespace, permission_list):
        '''
        Return `True` is at list one row was found, `False` otherwise.
        '''
        return True

    def __get_fullname(self, o):
        '''
        Return full namespace of object.
        '''
        return o.__module__ + "." + o.__class__.__name__

    def __get_project_instance(owner_username, project_name):
        '''
        Get project instance.
        '''
        proj_ins = None
        try:
            proj_ins = project.objects.get_by_natural_key(owner_username, project_name)
        except: raise Http404
        else:
            return proj_ins


    def __check_project_private(project_instance):
        '''
        Check if project is private.

        If one of or both arguments not provide, raise HTTP 404 error.
        '''
        return project_instance.is_private


    def __is_team_member(project_instance,  username):
        '''
        Check if a user is one of team member of the givn project.
        '''
        username_list = project_instance.objects.get_team_members_username()
        if isinstance(username_list, (tuple, list)):
            return username_list.count(username)
        else:
            raise False

        return True

    def __get_anonymous_permissions(self):
        # everybody all has anonymous permissions.
        anon_role_name = role(name=settings.ANONYMOUS_ROLE_NAME)
        user_ins = user.objects.get_by_natural_key(anon_role_name)
        pur_ins_list = project_user_role.objects.filter(project=self, user=user_ins)
        return pur_ins_list

    def __is_owner(project_instance, username):
        '''
        Check if a user is the owner of the givn project.
        '''
        if project_instance.user.username == username:
            return True
        else:
            return False
