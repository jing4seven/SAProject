from django.utils import timezone
from rest_framework import serializers

from api.secure.models import user
from .models import project, project_status, release, release_status, work_item_group, work_item


class project_serializer(serializers.Serializer):
	pk = serializers.Field()
	name = serializers.CharField(required=True, max_length=50)
	alias = serializers.CharField(required=True, max_length=250)	
	owner_id = serializers.IntegerField(required=True)
	owner_username = serializers.Field(source='owner.username')
	description = serializers.CharField(required=False)
	is_private = serializers.BooleanField(default=False)
	update_time = serializers.DateTimeField(default=timezone.now(), read_only=True)
	last_edited_by = serializers.CharField(required=True, max_length=250)
	
	class Meta:
		model = project
		fields = ('pk', 'name', 'alias', 'owner_id', 'owner_username', 'description', 'is_private', 'update_time', 'last_edited_by')
		read_only_fields =('owner_username', 'update_time',) 
		
	def restore_object(self, attrs, instance=None):			
		if instance is not None:
			instance.pk = attrs.get('pk', instance.pk)
			instance.name = attrs.get('name', instance.name)
			instance.alias = attrs.get('alias', instance.alias)
			input_owner_id = attrs.get('owner_id', None)
			if input_owner_id is not None:
				instance.owner = user.objects.get(pk=input_owner_id)
			instance.description = attrs.get('description', instance.description)
			instance.is_private = attrs.get('is_private', instance.is_private)
			instance.last_edited_by = attrs.get('last_edited_by', instance.last_edited_by)
			return instance
		
		return project(**attrs)
	
class project_status_serializer(serializers.Serializer):
	pk = serializers.Field()
	name = serializers.CharField(required=True, max_length=50)
	project_id = serializers.IntegerField(required=True)
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
				instance.project = project.objects.get(pk=input_project_id)
			instance.is_current = attrs.get('is_current', instance.is_current)
			instance.description = attrs.get('description', instance.description)
			return instance
		
		return project_status(**attrs)
	
class release_serializer(serializers.Serializer):
	pk = serializers.Field()
	name = serializers.CharField(required=True, max_length=250)
	project_id = serializers.IntegerField(required=True)
	description = serializers.CharField(required=False)
	deadline = serializers.DateTimeField(required=False)
	update_time = serializers.DateTimeField(default=timezone.now(), read_only=True)
	last_edited_by = serializers.CharField(required=True, max_length=250)
	
	class Meta:
		model = release
		fields = ('pk', 'name', 'project_id', 'description', 'deadline', 'update_time', 'last_edited_by')
		read_only_fields= ('update_time',)
		
	def restore_object(self, attrs, instance=None):
		if instance is not None:
			instance.pk = attrs.get('pk', instance.pk)
			instance.name = attrs.get('name', instance.name)
			input_project_id = attrs.get('project_id', None)
			if input_project_id is not None:
				instance.project = project.objects.get(pk=input_project_id)
			instance.description = attrs.get('description', instance.description)
			instance.deadline = attrs.get('deadline', instance.deadline)
			instance.last_edited_by = attrs.get('last_edited_by', instance.last_edited_by)
			return instance
		
		return release(**attrs)


class release_status_serializer(serializers.Serializer):
	pk = serializers.Field()
	name = serializers.CharField(required=True, max_length=50)
	release_id = serializers.IntegerField(required=True)
	is_current = serializers.BooleanField(default=False)
	description = serializers.CharField(required=False)
	
	class Meta:
		model = release_status
		fields = ('pk', 'name', 'release_id', 'is_current', 'description')	
		
	def restore_object(self, attrs, instance=None):
		if instance is not None:
			instance.pk = attrs.get('pk', instance.pk)
			instance.name = attrs.get('name', instance.name)
			input_release_id = attrs.get('release_id', None)
			if input_release_id is not None:
				instance.release = release.objects.get(pk=input_release_id)
			instance.is_current = attrs.get('is_current', instance.is_current)
			instance.description = attrs.get('description', instance.description)
			return instance
		
		return release_status(**attrs)
	
	
class work_item_group_serializer(serializers.Serializer):
	pk = serializers.Field()
	project_id = serializers.IntegerField(required=True)
	parent_id = serializers.IntegerField(required=False)
	name = serializers.CharField(required=True, max_length=250)
	description = serializers.CharField(required=False)
	importance = serializers.IntegerField(default=0)
	time_logged = serializers.IntegerField(default=0)
	initial_estimate = serializers.IntegerField(default=0)
	update_time = serializers.DateTimeField(default=timezone.now(), read_only=True)
	last_edited_by = serializers.CharField(required=True, max_length=250)
	
	class Meta:
		model = work_item_group
		fields = ('pk', 'project_id', 'parent_id', 'name', 'description', 'importance', 'time_logged', 'initial_estimate', \
				  'update_time', 'last_edited_by')
		read_only_fields = ('update_time',)
		
	def restore_object(self, attrs, instance=None):
		if instance is not None:
			instance.pk = attrs.get('pk', instance.pk)
			
			input_project_id = attrs.get('project_id', None)
			if input_project_id is not None:
				instance.project = project.objects.get(pk=input_project_id)
				
			input_parent_id = attrs.get('parent_id', None)
			if input_parent_id is not None:
				instance.parent = work_item_group.objects.get(pk=input_parent_id)
				
			instance.name = attrs.get('name', instance.name)
			instance.description = attrs.get('description', instance.description)
			instance.importance = attrs.get('importance', instance.importance)
			instance.time_logged = attrs.get('time_logged', instance.time_logged)
			instance.initial_estimate = attrs.get('initial_estimate', instance.initial_estimate)
			instance.last_edited_by = attrs.get('last_edited_by', instance.last_edited_by)
			return instance
		
		return work_item_group(**attrs)
	
	
class work_item_serializer(serializers.Serializer):
	pk = serializers.Field()
	work_item_group_id = serializers.IntegerField(required=True)
	release_id = serializers.IntegerField(required=False)
	parent_id = serializers.IntegerField(required=False)
	name = serializers.CharField(max_length=250, required=True)
	description = serializers.CharField(required=False)
	loe = serializers.IntegerField(default=0)
	creator_id = serializers.IntegerField(required=True)
	assignee_id = serializers.IntegerField(required=False)
	requestor_id = serializers.IntegerField(required=False)
	time_logged = serializers.IntegerField(default=0)
	update_time = serializers.DateTimeField(default=timezone.now(), read_only=True)
	last_edited_by = serializers.CharField(required=True, max_length=250)
	
	class Meta:
		model = work_item
		fields = ('pk', 'work_item_group_id', 'release_id', 'parent_id', 'name', 'description', 'loe', 'creator_id', \
				  'assignee_id', 'requestor_id', 'time_logged', 'update_time', 'last_edited_by')
		read_only_fields = ('update_time',)
		
	def restore_object(self, attrs, instance=None):
		if instance is not None:
			instance.pk = attrs.get('pk', instance.pk)
			
			input_work_item_group_id = attrs.get('work_item_group_id', None)
			if input_work_item_group_id is not None:
				instance.work_item_group = work_item_group.objects.get(pk=input_work_item_group_id)
				
			input_release_id = attrs.get('release_id', None)
			if input_release_id is not None:
				instance.release = release.objects.get(pk=input_release_id)
				
			input_parent_id = attrs.get('parent_id', None)
			if input_parent_id is not None:
				instance.parent = work_item.objects.get(pk=input_parent_id)	
				
			instance.name = attrs.get('name', instance.name)
			instance.description = attrs.get('description', instance.description)
			instance.loe = attrs.get('loe', instance.loe)
			
			input_creator_id = attrs.get('creator_id', None)
			if input_creator_id is not None:
				instance.creator = user.objects.get(pk=input_creator_id)
				
			input_assignee_id = attrs.get('assignee_id', None)
			if input_assignee_id is not None:
				instance.assignee = user.objects.get(pk=input_assignee_id)		
				
			input_requestor_id = attrs.get('requestor_id', None)
			if input_requestor_id is not None:
				instance.requestor = user.objects.get(pk=input_requestor_id)		
				
			instance.time_logged = attrs.get('time_logged', instance.time_logged)
			instance.last_edited_by = attrs.get('last_edited_by', instance.last_edited_by)
			return instance
		
		return work_item(**attrs)
				
				
				
				
				
				
				
				
				
				
				
				
				