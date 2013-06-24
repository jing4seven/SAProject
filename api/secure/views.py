from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from api.secure.models import user
from api.secure.serializers import user_serializer

class user_view(ListModelMixin, 
				CreateModelMixin, 
				GenericAPIView, 
				UpdateModelMixin, 
				RetrieveModelMixin,
				DestroyModelMixin):
	queryset = user.objects.all()
	serializer_class = user_serializer
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