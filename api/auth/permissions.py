from django.core.urlresolvers import reverse
from rest_framework import  permissions
from api.secure.models import project_user_role,  permission as permission_model, \
 endpoint
from api.secure.models import role as role_model

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
		# 1. How to get view's namespace here?  				DONE
		# 2. How to get project_name and owner_username here? 	DONE
		# 3. How to enable session data here?

		# super user has all permissions.
		if request.user.is_superuser:
			return True

		# check if project is PRIVATE
		project_is_private = False
		perm_parm_dict = {'owner_username':'', 'project_name':'', 'project_id': -1}
		perm_parm_dict.update(request.__dict__['parser_context']['kwargs'])

		owner_username = perm_parm_dict['owner_username']
		project_name = perm_parm_dict['project_name']
		project_id = perm_parm_dict['project_id']

		role_list = [role_model.get_anonymous_role_name()]

		if project_name and owner_username:
			project_is_private = self.__check_project_private(owner_username, project_name)
			if project_is_private and not __is_team_member(owner_username, project_name, request.user):
				# check if current user is team member.
				return False
			# get project role list
			role_list.append(self.__get_user_project_role_list(project_name, request.user))
		
		# clear repeate roles
		role_list = tuple(set(role_list))

		# get permission list
		permission_list = self.__get_permissions_by_roles(role_list)
		# get view namespace
		view_namespace = self.__get_fullname(view)

		return __has_permission_on_view(request.method, view_namespace, permission_list)

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

	def __check_project_private(owner_username,project_name):
		'''
		Check if project is private.

		If one of or both arguments not provide, rasie HTTP 404 error.
		'''
		from api.project.models import project
		return True

	def __get_user_project_role_list(project_name=None, username=None):
		'''
		Get user project role list.

		If one or both arguments not provide, return Anonymous role.
		'''
		return ()

	def __get_permissions_by_roles(role_list):
		'''
		Get roles for role list.
		'''
		return ()

	def __is_team_member(owner_username, project_name,  username):
		'''
		Check if a user is one of team member of the givn project.
		'''
		return True

	def __is_owner(project_name, username):
		'''
		Check if a user is the owner of the givn project.
		'''
		return True