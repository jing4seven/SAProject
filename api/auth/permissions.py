from rest_framework import  permissions


class api_permission(permissions.BasePermission):
	'''
	A implement class that match site client permission to socpes.
	'''
	def has_permission(self, request, view):
		"""
		Return `True` if permission is granted, `False` otherwise.
		"""
		return True

	def has_object_permission(self, request, view, obj):
		"""
		Return `True` if permission is granted, `False` otherwise.
		"""
		return True