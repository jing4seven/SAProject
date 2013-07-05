from rest_framework import  permissions
from api.secure.models import project_user_role,  permission as permission_model, \
 endpoint

class api_permission(permissions.BasePermission):
	'''
	A implement class that match site client permission to socpes.
	'''
	def has_permission(self, request, view):
		"""
		Return `True` if permission is granted, `False` otherwise.
		"""
		
		


		# raise BaseException(request.project_id)
		# return True

	def has_object_permission(self, request, view, obj):
		"""
		Return `True` if permission is granted, `False` otherwise.
		"""
		return True