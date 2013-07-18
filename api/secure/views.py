from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, \
UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from api.secure.serializers import user_serializer, role_serializer, \
permission_serializer
from api.secure.models import user

class users_view(GenericAPIView,ListModelMixin):
    queryset = user.objects.all()
    serializer_class = user_serializer

    def get(self, request ):
        return self.list(request)


class user_view(GenericAPIView,
                CreateModelMixin,
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
        return self.retrieve(request, username , format=format)

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


class project_user_role_view(GenericAPIView,
                             CreateModelMixin,
                             DestroyModelMixin):
    pass

class project_users_view(GenericAPIView, ListModelMixin):
    pass
