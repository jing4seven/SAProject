from django.utils import timezone
from rest_framework import serializers

from api.secure.models import user
from api.secure.serializers import user_serializer
from .models import project, project_status


class project_serializer(serializers.Serializer):
	pk = serializers.Field()
	name = serializers.CharField(required=True, max_length=50)
	alias = serializers.CharField(required=True, max_length=250)	
	owner_id = serializers.WritableField(source='owner.id', required=True)
	#owner_username = serializers.Field(source='owner.username')
	description = serializers.CharField(required=False)
	is_private = serializers.BooleanField(default=False)
	update_time = serializers.DateTimeField(default=timezone.now(), read_only=True)
	last_edited_by = serializers.CharField(required=True, max_length=250)
	
	class Meta:
		model = project
		fields = ('pk', 'name', 'alias', 'owner_id', 'description', 'is_private', 'update_time', 'last_edited_by')
		read_only_fields =('update_time',) 
		
	def restore_object(self, attrs, instance=None):			
		if instance is not None:
			instance.pk = attrs.get('pk', instance.pk)
			instance.name = attrs.get('name', instance.name)
			instance.alias = attrs.get('alias', instance.alias)
			input_owner_id = attrs.get('owner_id', None)
			if input_owner_id is not None:
				instance.own = user.objects.get(input_owner_id)
			instance.description = attrs.get('description', instance.description)
			instance.is_private = attrs.get('is_private', instance.is_private)
			instance.last_edited_by = attrs.get('last_edited_by', instance.last_edited_by)
			return instance
		
		return project(**attrs)
	
class project_status_serializer(serializers.Serializer):
	pk = serializers.Field()
	name = serializers.CharField(required=True, max_length=50)
	project_id = serializers.WritableField(source='project.id', required=True)
	is_current = serializers.BooleanField(default=False)
	description = serializers.CharField(required=False)
	
	class Meta:
		model = project_status
		fields = ('pk', 'name', 'project_id', 'is_current', 'description')
		
	def restore_object(self, attrs, instance=None):
		if instance is not None:
			instance.pk = attrs.get('pk', instance.pk)
			instance.name = attrs.get('name', instance.name)
			input_project_id = attrs.get('project_id', None)
			if input_project_id is not None:
				instance.project = project.objects.get(project_id)
			instance.is_current = attrs.get('is_current', instance.is_current)
			instance.description = attrs.get('description', instance.description)
			return instance
		
		return project_status(**attrs)
	
		