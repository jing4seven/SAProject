from django.http import Http404
from rest_framework import generics
from rest_framework import mixins


from api.secure.models import user
from .models import project, project_status
from .serializers import project_serializer, project_status_serializer


class projects_view(generics.GenericAPIView,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = project.objects.all()
    serializer_class = project_serializer
    #lookup_field = 'owner.id'
    
    def get(self, request, owner_id=0):
        if owner_id > 0:
            self.kwargs['owner.pk'] = owner_id
            
        return self.list(request, format=format)
    
    def post(self, request):        
        return self.create(request, format=format)
    
    def get_queryset(self):
        if 'owner.pk' in self.kwargs:
            try:
                owner = user.objects.get(pk=self.kwargs['owner.pk'])
                return project.objects.filter(owner=owner)
            except user.DoesNotExist:
                return project.objects.get_empty_query_set()
                
        return project.objects.all()
        
    

class project_view(generics.GenericAPIView,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin):
    
    queryset = project.objects.all()
    serializer_class = project_serializer
    
    def get(self, request, pk=0):        
        return self.retrieve(request, pk=pk, format=format)
       
    def post(self, request, pk=0):        
        return self.create(request, pk=pk, format=format)

    def put(self, request, pk=0):
        return self.update(request, pk=pk, format=format)

    def delete(self, request, pk=0):
        return self.destroy(request, pk=pk, format=format)
    
class project_status_view(generics.GenericAPIView,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin):
    queryset = project_status.objects.all()
    serializer_class = project_status_serializer
    lookup_field = 'name'
    
    def get(self, request, owner_username="", project_name="", name="", format='json'):
        if len(owner_username) > 0 and len(project_name) > 0 and len(name) > 0:
            self._set_queryset(owner_username, project_name, name)       
            return self.retrieve(request)     
        elif len(owner_username) > 0 and len(project_name) > 0:
            self._set_queryset(owner_username, project_name)
            return self.list(request)

    def post(self, request, owner_username="", project_name="", format='json'):        
        return self.create(request, format=format)

    def put(self, request, owner_username="", name="", format='json'):
        if len(owner_username) > 0:
            self._set_queryset(owner_username)
            
        return self.update(request, name=name, format=format)

    def delete(self, request, owner_username="", name="", format='json'):
        if len(owner_username) > 0:
            self._set_queryset(owner_username)

        return self.destroy(request, name=name, format=format)

    def _set_queryset(self, owner_username="", name=""):        
        try:
            owner = user.objects.get(username=owner_username)
            if len(name) > 0:
                self.queryset = project.objects.filter(owner_id=owner.pk, name=name)
            else:
                self.queryset = project.objects.filter(owner_id=owner.pk)
        except:
            raise Http404
    