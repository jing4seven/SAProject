import re
from django.utils import timezone
from rest_framework import serializers
from api.auth.models import auth_hmac

class api_auth_serializer(serializers.ModelSerializer):
	'''
	Serializer of api_auth
	'''
	pk = serializers.Field()
	client_id = serializers.CharField(required=False, read_only=True)
	security_key = serializers.CharField(required=False, read_only=True)
	scope = serializers.CharField(required=False)
	enable = serializers.BooleanField(required=False)

	class Meta:
		model = auth_hmac
		fields = ('pk', 'name', 'description', 'client_id', 'security_key', 'scope', 'created_time')
		ordering = ('created_time',)

	def restore_object(self, attrs, instance=None):
		'''
		Deserialize the object

		If this method not defined, then deserializing data will simply return a dictionary of items.
		When invoke "serializer.save", 'dict' object has no attribute 'save' error will be raised.
		'''
		if instance:
			instance.name = attrs.get('name', instance.name)
			instance.description = attrs.get('description', instance.description)
			instance.client_id = attrs.get('client_id', instance.client_id)
			instance.security_key = attrs.get('security_key', instance.security_key)
			instance.scope = attrs.get('scope', instance.scope)
			instance.enable = attrs.get('enable', instance.enable)
			instance.created_time = attrs.get('created_time', instance.created_time)
			return instance

		return auth_hmac(**attrs)

	def validate(self, attrs):
		if not re.match(r'^([a-zA-Z|\ |0-9]){5,50}$', attrs['name']):
			raise serializers.ValidationError("'name' filed should only be character, numbers and blank which between 5 - 50 long.")

		return attrs