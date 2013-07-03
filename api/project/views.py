from rest_framework import generics
from rest_framework import mixins


from api.secure.models import user
from .models import project, project_status, release, release_status, work_item_group, work_item
from .serializers import project_serializer, project_status_serializer, release_serializer, \
                         release_status_serializer, work_item_group_serializer, work_item_serializer


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

class release_status_list_view(generics.GenericAPIView,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin):
    queryset = release_status.objects.all()
    serializer_class = release_status_serializer
    
    def get(self, request, release_id):
        if release_id > 0:
            self.kwargs['release.pk'] = release_id
            
        return self.list(request)
    
    def post(self, request, release_id):
        if release_id > 0:
            self.kwargs['release.pk'] = release_id
            
        return self.create(request)
    
    def get_queryset(self):
        if 'release.pk' in self.kwargs:
            try:
                input_release = release.objects.get(pk=self.kwargs['release.pk'])
                return release_status.objects.filter(release=input_release)
            except release.DoesNotExist:
                return release_status.objects.filter(release=None)
            
        return release_status.objects.all()
    
class release_status_detail_view(generics.GenericAPIView,
                                 mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin):
    
    queryset = release_status.objects.all()
    serializer_class = release_status_serializer
    
    def get(self, request, release_status_id=0):    
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = release_status_id  
            
        return self.retrieve(request)
    
    def post(self, request, release_status_id=0):
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = release_status_id  
            
        if release_status_id > 0:
            try:
                release_status.objects.get(pk=release_status_id)
                return self.update(request)
            except release.DoesNotExist:
                return self.create(request)
                    
        return self.create(request)

    def put(self, request, release_status_id=0):
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = release_status_id  
         
        return self.update(request)

    def delete(self, request, release_status_id=0):
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = release_status_id  
         
        return self.destroy(request)
    
class work_item_groups_view(generics.GenericAPIView,
                            mixins.CreateModelMixin,
                            mixins.ListModelMixin):
    queryset = work_item_group.objects.all()
    serializer_class = work_item_group_serializer
    
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
                return work_item_group.objects.filter(project=input_project)
            except project.DoesNotExist:
                return work_item_group.objects.filter(project=None)
        
        return work_item_group.objects.all()
    
class work_item_group_view(generics.GenericAPIView,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin):
    queryset = work_item_group.objects.all()
    serializer_class = work_item_group_serializer
    
    def get(self, request, work_item_group_id=0):    
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = work_item_group_id  
             
        return self.retrieve(request)
       
    def post(self, request, work_item_group_id=0):  
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = work_item_group_id  
               
        if work_item_group_id > 0:
            try:
                work_item_group.objects.get(pk=work_item_group_id)
                return self.update(request)
            except release.DoesNotExist:
                return self.create(request)
               
        return self.create(request)

    def put(self, request, work_item_group_id=0):  
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = work_item_group_id  
               
        return self.update(request)

    def delete(self, request, work_item_group_id=0):  
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = work_item_group_id  
               
        return self.destroy(request)
        
class work_items_by_group_view(generics.GenericAPIView,
                              mixins.CreateModelMixin,
                              mixins.ListModelMixin):
    queryset = work_item.objects.all()
    serializer_class = work_item_serializer
    
    def get(self, request, work_item_group_id=0):
        if work_item_group_id > 0:
            self.kwargs['work_item_group.pk'] = work_item_group_id
            
        return self.list(request)
    
    def post(self, request, work_item_group_id=0):
        if work_item_group_id > 0:
            self.kwargs['work_item_group.pk'] = work_item_group_id
        
        return self.create(request)
    
    def get_queryset(self):
        if 'work_item_group.pk' in self.kwargs:
            try:
                input_work_item_group = work_item_group.objects.get(pk=self.kwargs['work_item_group.pk'])
                return work_item.objects.filter(work_item_group=input_work_item_group)
            except project.DoesNotExist:
                return work_item.objects.filter(work_item_group=None)
        
        return work_item.objects.all()
      
class work_items_by_release_view(generics.GenericAPIView,
                                 mixins.CreateModelMixin,
                                 mixins.ListModelMixin):
    queryset = work_item.objects.all()
    serializer_class = work_item_serializer
    
    def get(self, request, release_id=0):
        if release_id > 0:
            self.kwargs['release.pk'] = release_id
            
        return self.list(request)
    
    def post(self, request, release_id=0):
        if release_id > 0:
            self.kwargs['release.pk'] = release_id
        
        return self.create(request)
    
    def get_queryset(self):
        if 'release.pk' in self.kwargs:
            try:
                input_release = release.objects.get(pk=self.kwargs['release.pk'])
                return work_item.objects.filter(release=input_release)
            except project.DoesNotExist:
                return work_item.objects.filter(release=None)
        
        return work_item.objects.all()
       
class work_item_view(generics.GenericAPIView,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    queryset = work_item.objects.all()
    serializer_class = work_item_serializer
    
    def get(self, request, work_item_id=0):    
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = work_item_id  
             
        return self.retrieve(request)
       
    def post(self, request, work_item_id=0):  
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = work_item_id  
               
        if work_item_id > 0:
            try:
                work_item.objects.get(pk=work_item_id)
                return self.update(request)
            except release.DoesNotExist:
                return self.create(request)
               
        return self.create(request)

    def put(self, request, work_item_id=0):  
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = work_item_id  
               
        return self.update(request)

    def delete(self, request, work_item_id=0):  
        if 'pk' not in self.kwargs:
            self.kwargs['pk'] = work_item_id  
               
        return self.destroy(request)
    