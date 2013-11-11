from django.http import Http404
from django.conf import settings
from django.core.cache import cache
from rest_framework import  permissions
from api.secure.models import role, project_user_role, role_permission
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

        All permissions will cached by role name.
        """

        # super user has all permissions.
        if request.user.is_superuser:
            return True

        project_is_private = False
        perm_parm_dict = {'owner_username':'', 'project_name':''}
        perm_parm_dict.update(request.parser_context['kwargs'])

        owner_username = perm_parm_dict['owner_username']
        project_name = perm_parm_dict['project_name']
        perm_list = []

        all_perms = cache.get(settings.PERMISSIONS_CACHED_KEY)
        if not all_perms:
            all_role = role.objects.all()
            all_perms = {}
            for r in all_role:
                p_list = []
                rp_ins_list = role_permission.objects.filter(role=r)
                for rp in rp_ins_list:
                    p_dict = {}
                    p_dict['codename'] = rp.permission.endpoint.codename
                    p_dict['GPPD'] = rp.permission.GPPD
                    p_list.append(p_dict)
                all_perms[r.name] = p_list
            # default expire time is 1 day, which confied in settings.py
            cache.set(settings.PERMISSIONS_CACHED_KEY, all_perms)

        if project_name and owner_username:
            proj_ins = self.__get_project_instance(owner_username, project_name)
            project_is_private = self.__check_project_private(proj_ins)
            # check if project is PRIVATE
            if project_is_private and not self.__is_team_member(proj_ins, request.user):
                # check if current user is team member.
                return False

            pur_ins_list = project_user_role.objects.filter(project=proj_ins, user=request.user)
            for pur in pur_ins_list:
                perm_list.extend(all_perms[pur.role.name])
            # all users has anonymous' permission
            perm_list.extend(all_perms[settings.ANONYMOUS_ROLE_NAME])

        if not len(perm_list):
            perm_list = all_perms[settings.ANONYMOUS_ROLE_NAME]

        # get view namespace
        view_namespace = self.__get_fullname(view)
        GPPD = settings.GPPD[request.method.upper()]
        return self.__has_permission_on_view(GPPD, view_namespace, perm_list)

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def __has_permission_on_view(self, method, view_namespace, permission_list):
        '''
        Return `True` is at list one row was found, `False` otherwise.
        '''
        #raise BaseException(method, view_namespace)
        for p in permission_list:
            if p['codename'] == view_namespace and p['GPPD'] == method:
                return True

        return False

    def __get_fullname(self, o):
        '''
        Return full namespace of object.
        '''
        return o.__module__ + "." + o.__class__.__name__

    def __get_project_instance(self, owner_username, project_name):
        '''
        Get project instance.
        '''
        proj_ins = None
        try:            
            proj_ins = project.objects.get_by_natural_key(owner_username, project_name)
        except: raise Http404
        else:
            return proj_ins


    def __check_project_private(self, project_instance):
        '''
        Check if project is private.

        If one of or both arguments not provide, raise HTTP 404 error.
        '''
        return project_instance.is_private


    def __is_team_member(self, project_instance,  username):
        '''
        Check if a user is one of team member of the givn project.
        '''
        username_list = project_instance.objects.get_team_members_username()

        if isinstance(username_list, (tuple, list)):
            return username_list.count(username)
        else:
            raise False

        return True


    def __is_owner(self, project_instance, username):
        '''
        Check if a user is the owner of the givn project.
        '''
        if project_instance.user.username == username:
            return True
        else:
            return False
