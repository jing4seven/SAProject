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
    
    def get(self, request, owner_id=0):
        if owner_id > 0:
            self.kwargs['owner.pk'] = owner_id
            
        return self.list(request)
    
    def post(self, request):        
        return self.create(request)
    
    def get_queryset(self):
        if 'owner.pk' in self.kwargs:
            try:
                owner = user.objects.get(pk=self.kwargs['owner.pk'])
                return project.objects.filter(owner=owner)
            except user.DoesNotExist:
                return project.objects.get_empty_query_set()
                
        return project.objects.all()
        
    

class project_view(generics.GenericAPIView,
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
    
class project_status_list_view(generics.GenericAPIView,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin):
    queryset = project_status.objects.all()
    serializer_class = project_status_serializer    
    
    def get(self, request, project_id=0):
        if project_id > 0:
            self.kwargs['project.pk'] = project_id
            
        return self.list(request)

    def post(self, request, pk=0):        
        return self.create(request, pk=pk)
    
    def get_queryset(self):
        if 'project.pk' in self.kwargs:
            try:
                input_project = project.objects.get(pk=self.kwargs['project.pk'])
                return project_status.objects.filter(project=input_project)
            except project.DoesNotExist:
                return project_status.objects.get_empty_query_set()
                
        return project_status.objects.all()
    
class project_status_detail_view(generics.GenericAPIView,
                                 mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin):
    
    queryset = project_status.objects.all()
    serializer_class = project_status_serializer
    
    def get(self, request, pk=0):        
        return self.retrieve(request, pk=pk)
       
    def post(self, request, pk=0):        
        return self.create(request, pk=pk)

    def put(self, request, pk=0):
        return self.update(request, pk=pk)

    def delete(self, request, pk=0):
        return self.destroy(request, pk=pk)
    