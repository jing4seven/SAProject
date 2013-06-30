import re
from datetime import datetime
from rest_framework import serializers
from api.secure.models import user, role, permission, project_user_role, \
endpoint, role_permission
from lib import validation

class user_serializer(serializers.ModelSerializer):
	pk = serializers.Field()
	client_id = serializers.CharField(source="get_client_id")
	full_name = serializers.CharField(required=False, read_only=True)
	age = serializers.Field(source="get_age")
	birthday = serializers.DateTimeField(required=False)
	# ToDo: Make this field available.
	# avatar = serializers.CharField(required=False, blank=True)
	last_login = serializers.DateTimeField(required=False, read_only=True)
	date_join = serializers.DateTimeField(required=False, read_only=True)
	is_supperuser = serializers.BooleanField(required=False, read_only=True)
	is_stuff = serializers.BooleanField(required=False, read_only=True)
	update_time = serializers.DateTimeField(required=False, read_only=True)

	class Meta:
		model = user
		fields = ('pk', 'client_id','full_name', 'username', 'password', \
			'first_name', 'last_name', 'disable', 'age', 'birthday',  'last_login',\
			 'is_supperuser', 'is_stuff', 'update_time', 'last_edited_by')
		ordering = ('-last_join', )

	def restore_object(self, attrs, instance=None):
		if instance is not None:
			instance.client_id = attrs.get('client_id', instance.client_id)
			instance.full_name = attrs.get('full_name', instance.full_name)
			instance.username = attrs.get('username', instance.username)
			instance.password = attrs.get('password', instance.password)
			instance.first_name = attrs.get('first_name', instance.first_name)
			instance.last_name = attrs.get('last_name', instance.last_name)
			instance.birthday = attrs.get('birthday', instance.birthday)
			instance.age = attrs.get('birthday', instance.birthday)
			instance.avatar = attrs.get('avatar', instance.avatar)
			instance.last_login = attrs.get('last_login', instance.last_login)
			instance.date_join = attrs.get('date_join', instance.date_join)
			instance.is_supperuser = attrs.get('is_supperuser', instance.is_supperuser)
			instance.is_stuff = attrs.get('is_stuff', instance.is_stuff)
			instance.update_time = attrs.get('update_time', instance.update_time)
			instance.last_edited_by = attrs.get('last_edited_by', instance.last_edited_by)
			return instance

		return user(**attrs)

	def validate(self, attrs):
		if not validation.check_char_basic(str.rstrip(str(attrs['username'])), 5, 50):
			raise serializers.ValidationError("'name' filed should only be character, \
				numbers and blank which between 5 - 50 long.")
		return attrs

class endpoint(serializers.ModelSerializer):
	pk = serializers.Field()
	name = serializers.CharField()
	codename = serializers.CharField()

	class Meta:
		model = endpoint
		fields = ('pk', 'name', 'codename')

class permission_serializer(serializers.ModelSerializer):
	pk = serializers.Field()
	name = serializers.CharField()
	endpoint = serializers.RelatedField(many=False)
	GPPD = serializers.IntegerField()

	class Meta:
		model = permission
		fields = ('pk', 'name', 'endpoint', 'GPPD')

class role_serializer(serializers.ModelSerializer):
	pk = serializers.Field()
	name = serializers.CharField()
	description = serializers.CharField(required=False)

	class Meta:
		model = role
		fields = ('pk', 'name', 'description')


class role_permission(serializers.ModelSerializer):
	pk = serializers.Field()
	role = serializers.RelatedField(many=False)
	permission = serializers.RelatedField(many=False)


class project_user_role(serializers.ModelSerializer):
	project = serializers.RelatedField(many=False)
	user = serializers.RelatedField(many=False)
	role = serializers.RelatedField(many=False)

	class Meta:
		model = project_user_role
		fields = ('pk', 'project', 'user', 'role')

