import re
from rest_framework import serializers
from api.auth.models import site_client as site_client_model
from django.core.urlresolvers import reverse

class api_auth_serializer(serializers.ModelSerializer):
    '''
    Serializer of api_auth
    '''

    class Meta:
        model = site_client_model
        fields = ('id', 'name', 'description', 'client_id', 'security_key',
                  'scope', 'created_time',)
        read_only_fields = ('client_id', 'security_key',)
        ordering = ('created_time',)

    def restore_object(self, attrs, instance=None):
        '''
        Deserialize the object

        If this method not defined, then deserializing data will simply return a dictionary of items.
        When invoke "serializer.save", 'dict' object has no attribute 'save' error will be raised.
        '''
        if not instance is None:
            instance.name = attrs.get('name', instance.name)
            instance.description = attrs.get('description', instance.description)
            instance.site_client_id = attrs.get('site_client_id', instance.site_client_id)
            instance.client_id = attrs.get('client_id', instance.client_id)
            instance.security_key = attrs.get('security_key', instance.security_key)
            instance.scope = attrs.get('scope', instance.scope)
            instance.enable = attrs.get('enable', instance.enable)
            instance.created_time = attrs.get('created_time', instance.created_time)
            return instance

        return site_client_model(**attrs)

    def validate(self, attrs):
        if not re.match(r'^([a-zA-Z|\ |0-9]){5,50}$', attrs['name']):
            raise serializers.ValidationError("'name' filed should only be character, numbers or blank which between 5 - 50 long.")
        return attrs
