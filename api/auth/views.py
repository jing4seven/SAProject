from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin,\
 UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from api.auth.permissions import api_permission
from api.auth.models import site_client as site_client_model
from api.auth.serializers import api_auth_serializer

class site_clients_view(GenericAPIView, ListModelMixin):
    '''
    Site Client View for handle Get request for list result.

    Support pagination.
    '''
    # authentication_classes = (api_auth, )
    # permission_classes= (api_permission,)
    serializer_class = api_auth_serializer
    queryset = site_client_model.objects.all()

    def get(self, request, **kwargs):
        return self.list(request)

    def _set_queryset(self, pk):
        try:
            queryset = site_client_model.objects.get(pk=pk)
        except site_client_model.DoesNotExist:
            raise Http404


class site_client_view(GenericAPIView,
                CreateModelMixin,
                UpdateModelMixin,
                RetrieveModelMixin,
                DestroyModelMixin):
    '''
    Site Client View for handle CRUD for site client.
    '''
    # authentication_classes = (api_auth, )
    #permission_classes= (api_permission,)
    queryset = site_client_model.objects.all()
    serializer_class = api_auth_serializer

    def get(self, request, pk=None, format='json', *args, **kwargs):
        '''
        Get site client list or one specified one record.
        '''
        if not pk:
            self._set_queryset(pk)
            return self.retrieve(request, pk, format=format)
        else:
            return self.retrieve(request)

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
            queryset = site_client_model.objects.get(pk=pk)
        except site_client_model.DoesNotExist:
            raise Http404
