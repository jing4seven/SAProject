import re
from rest_framework import serializers
from api.secure.model import user, role, permission, content_type, user_permission, role_permission, user_role
from lib import validation

class user_serializer(serializers.ModelSerializer):
	pk = serializers.Field()
	full_name = serializers.CharField(required=False, read_only=True)
	username = serializers.CharField()
	password = serializers.CharField()
	first_name = serializer.CharField()
	last_name = serializers.CharField()
	disable = serializers.BooleanField()
	age = serializers.PositiveSmallIntegerField(required=False, read_only=True)
	birthday = serializers.DateTimeField()
	avatar = serializers.CharField()
	last_login = serializers.DateTimeField(required=False, read_only=True)
	date_join = serializers.DateTimeField(required=False, read_only=True)
	is_supperuser = serializers.BooleanField(required=False, read_only=True)
	is_stuff = serializers.BooleanField(required=False, read_only=True)
	update_time = serializers.DateTimeField(required=False, read_only=True)
	last_edited_by = serializers.CharField(required=False, read_only=True)

	class Meta:
		model = user
		fields = ('pk', 'full_name', 'username', 'password', 'first_name', 'last_name', 'disable', 'age', 'birthday', 'last_login', 'is_supperuser', 'is_stuff', 'update_time', 'last_edited_by')
		ordering = ('-last_join', )

	def restore_object(self, attrs, instance=None):
		if instance is not None:
			instance.full_name = attrs.get('full_name', instance.full_name)
			instance.username = attrs.get('username', instance.username)
			instance.password = attrs.get('password', instance.password)
			instance.first_name = attrs.get('first_name', instance.first_name)
			instance.last_name = attrs.get('last_name', instance.last_name)
			instance.age = attrs.get('age', instance.age)
			instance.birthday = attrs.get('birthday', instance.birthday)
			instance.avatar = attrs.get('avatar', instance.birthday)
			instance.last_login = attrs.get('last_login', instance.last_login)
			instance.date_join = attrs.get('date_join', instance.date_join)
			instance.is_supperuser = attrs.get('is_supperuser', instance.is_supperuser)
			instance.is_stuff = attrs.get('is_stuff', instance.is_stuff)
			instance.update_time = attrs.get('update_time', instance.update_time)
			instance.last_edited_by = attrs.get('last_edited_by', instance.last_edited_by)
			return instance

		return user(**attrs)

	def validate(self, attrs):
		if not validation.check_char_basic(str.rstrip(attrs['name']), 5, 50):
			raise serializers.ValidationError("'name' filed should only be character, numbers and blank which between 5 - 50 long.")
		return attrs

