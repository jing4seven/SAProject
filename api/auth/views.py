from django.http import Http404
from rest_framework import exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response
from api.auth.authentication import api_auth
from api.auth.models import auth_hmac
from api.auth.serializers import api_auth_serializer

class site_client(ListModelMixin, 
				CreateModelMixin, 
				GenericAPIView, 
				UpdateModelMixin, 
				RetrieveModelMixin,
				DestroyModelMixin):
	'''
	Site Client View for handle CRUD for site client.

	Support pagination.
	'''
	# authentication_classes = (api_auth, )
	# permission_classes((api_permission,)
	queryset = auth_hmac.objects.all()
	serializer_class = api_auth_serializer

	def get(self, request, pk=0, format='json'):
		'''
		Get site client list or one specified one record.
		'''
		if not pk==0:
			self._set_queryset(pk)
			return self.retrieve(request, pk, format=format)
		else:
			return self.list(request)

	def post(self, request, format='json'):
		'''
		Create a new site client.
		'''
		return self.create(request, format=format)

	def put(self, request, pk=0, format='json'):
		'''
		Update a specified site client.
		'''
		self._set_queryset(pk)

		return self.update(request, format=format)

	def delete(self, request, pk=0, format='json'):
		'''
		Delete one object.
		'''
		self._set_queryset(pk)

		return self.destroy(request, format=format)

	def _set_queryset(self, pk):
		try:
			queryset = auth_hmac.objects.get(pk=pk)
		except auth_hmac.DoesNotExist:
			raise Http404