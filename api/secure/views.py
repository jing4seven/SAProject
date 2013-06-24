from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from api.secure.models import user, role, permission
from api.secure.serializers import user_serializer, role_serializer, permission_serializer

class user_view(ListModelMixin, 
				CreateModelMixin, 
				GenericAPIView, 
				UpdateModelMixin, 
				RetrieveModelMixin,
				DestroyModelMixin):
	queryset = user.objects.all()
	serializer_class = user_serializer
	# override query key in url 
	# such as: /secure/username
	# default value is pk which is the primary key of this table.
	lookup_field = 'username'

	def get(self, request, username="", format='json'):
		if not len(username)==0:
			self._set_queryset(username)
			# pk = self.get_queryset()[0].pk
			return self.retrieve(request, username , format=format)
		else:
			return self.list(request)

	def post(self, request, format='json'):
		return self.create(request, format=format)

	def put(self, request, username="", format='json'):
		self._set_queryset(username)

		return self.update(request, format=format)

	def delete(self, request, username="", format='json'):
		self._set_queryset(username)

		return self.destroy(request, format=format)

	def _set_queryset(self, username):
		try:
			queryset = user.objects.get(username=username)
		except:
			raise Http404

class role_view(ListModelMixin, 
				CreateModelMixin, 
				GenericAPIView, 
				UpdateModelMixin, 
				RetrieveModelMixin,
				DestroyModelMixin):
	queryset = role.objects.all()
	serializer_class = role_serializer
	lookup_field = 'name'

	def get(self, request, name="", format='json'):
		if not len(name)==0:
			self._set_queryset(name)
			return self.retrieve(request, name , format=format)
		else:
			return self.list(request)

	def post(self, request, format='json'):
		return self.create(request, format=format)

	def put(self, request, name="", format='json'):
		self._set_queryset(name)

		return self.update(request, format=format)

	def delete(self, request, name="", format='json'):
		self._set_queryset(name)

		return self.destroy(request, format=format)

	def _set_queryset(self, name):
		try:
			queryset = role.objects.get(name=name)
		except:
			raise Http404

class permission_view(ListModelMixin, 
				CreateModelMixin, 
				GenericAPIView, 
				UpdateModelMixin, 
				RetrieveModelMixin,
				DestroyModelMixin):
	queryset = permission.objects.all()
	serializer_class = permission_serializer
	lookup_field = 'name'

	def get(self, request, name="", format='json'):
		if not len(name)==0:
			self._set_queryset(name)
			return self.retrieve(request, name , format=format)
		else:
			return self.list(request)

	def post(self, request, format='json'):
		return self.create(request, format=format)

	def put(self, request, name="", format='json'):
		self._set_queryset(name)

		return self.update(request, format=format)

	def delete(self, request, name="", format='json'):
		self._set_queryset(name)

		return self.destroy(request, format=format)

	def _set_queryset(self, name):
		try:
			queryset = permission.objects.get(name=name)
		except:
			raise Http404