from rest_framework import generics
from rest_framework import mixins


from api.secure.models import user
from .models import project, project_status, release
from .serializers import project_serializer, project_status_serializer, release_serializer


class projects_view(generics.GenericAPIView,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = project.objects.all()
    serializer_class = project_serializer
    
    def get(self, request, owner_id=0):
        if owner_id > 0:
            self.kwargs['owner.pk'] = owner_id
            
        return self.list(request)
    
    def post(self, request, owner_id=0):        
        return self.create(request, owner_id=owner_id)
    
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
    
    def get(self, request, project_id=0):      
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = project_id  
            
        return self.retrieve(request)
       
    def post(self, request, project_id=0):  
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = project_id 
                  
        return self.create(request)

    def put(self, request, project_id=0):
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = project_id 
        
        return self.update(request)

    def delete(self, request, project_id=0):
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = project_id 
            
        return self.destroy(request)
    
class project_status_list_view(generics.GenericAPIView,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin):
    queryset = project_status.objects.all()
    serializer_class = project_status_serializer    
    
    def get(self, request, project_id=0):
        if project_id > 0:
            self.kwargs['project.pk'] = project_id
            
        return self.list(request)

    def post(self, request, project_id=0): 
        if project_id > 0:
            self.kwargs['project.pk'] = project_id
                   
        return self.create(request)
    
    def get_queryset(self):
        if 'project.pk' in self.kwargs:
            try:
                input_project = project.objects.get(pk=self.kwargs['project.pk'])
                return project_status.objects.filter(project=input_project)
            except project.DoesNotExist:
                return project_status.objects.filter(project=None)
                
        return project_status.objects.all()
    
class project_status_detail_view(generics.GenericAPIView,
                                 mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin):
    
    queryset = project_status.objects.all()
    serializer_class = project_status_serializer
    
    def get(self, request, project_status_id=0):    
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = project_status_id  
            
        return self.retrieve(request)
    
    def post(self, request, project_status_id=0):
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = project_status_id  
            
        if project_status_id > 0:
            try:
                project_status.objects.get(pk=project_status_id)
                return self.update(request)
            except release.DoesNotExist:
                return self.create(request)
                    
        return self.create(request)

    def put(self, request, project_status_id=0):
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = project_status_id  
         
        return self.update(request)

    def delete(self, request, project_status_id=0):
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = project_status_id  
         
        return self.destroy(request)
    
class releases_view(generics.GenericAPIView,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    queryset = release.objects.all()
    serializer_class = release_serializer
    
    def get(self, request, project_id=0):
        if project_id > 0:
            self.kwargs['project.pk'] = project_id
            
        return self.list(request)

    def post(self, request, project_id=0):   
        if project_id > 0:
            self.kwargs['project.pk'] = project_id
             
        return self.create(request)
    
    def get_queryset(self):
        if 'project.pk' in self.kwargs:
            try:
                input_project = project.objects.get(pk=self.kwargs['project.pk'])
                return release.objects.filter(project=input_project)
            except project.DoesNotExist:
                return release.objects.get_empty_query_set()
                
        return release.objects.all()
    
    
class release_view(generics.GenericAPIView,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin):
    
    queryset = release.objects.all()
    serializer_class = release_serializer
    
    def get(self, request, release_id=0):    
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = release_id  
             
        return self.retrieve(request)
       
    def post(self, request, release_id=0):  
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = release_id  
               
        if release_id > 0:
            try:
                release.objects.get(pk=release_id)
                return self.update(request)
            except release.DoesNotExist:
                return self.create(request)
               
        return self.create(request)

    def put(self, request, release_id=0):  
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = release_id  
               
        return self.update(request)

    def delete(self, request, release_id=0):  
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = release_id  
               
        return self.destroy(request)
    