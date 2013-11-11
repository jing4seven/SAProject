from rest_framework import serializers, relations
from api.secure.models import user, role, permission, project_user_role, \
endpoint, role_permission
from lib import validation

class user_serializer(serializers.ModelSerializer):
    full_name = serializers.Field(source="get_full_name")
    age = serializers.Field(source="get_age")
    ## ToDo: Make this field available.
    ## avatar = serializers.CharField(required=False, blank=True)
    site_client = relations.HyperlinkedRelatedField(many=False,
                                                    view_name='site_client',
                                                    read_only=True)

    class Meta:
        model = user
        fields = ('username', 'password',
            'full_name', 'first_name', 'last_name', 'age', 'birthday',
                  'site_client','last_login',
            'is_staff', 'update_time', 'last_edited_by')
        ordering = ('-last_join', )

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.site_client_id = attrs.get('site_client_id',
                                                instance.site_client_id)
            instance.username = attrs.get('username', instance.username)
            instance.password = attrs.get('password', instance.password)
            instance.first_name = attrs.get('first_name', instance.first_name)
            instance.last_name = attrs.get('last_name', instance.last_name)
            instance.birthday = attrs.get('birthday', instance.birthday)
            instance.age = attrs.get('birthday', instance.birthday)
            instance.avatar = attrs.get('avatar', instance.avatar)
            instance.last_login = attrs.get('last_login', instance.last_login)
            instance.date_join = attrs.get('date_join', instance.date_join)
            instance.is_supperuser = attrs.get('is_supperuser',
                                               instance.is_supperuser)
            instance.is_staff = attrs.get('is_staff', instance.is_staff)
            instance.update_time = attrs.get('update_time', instance.update_time)
            instance.last_edited_by = attrs.get('last_edited_by',
                                                instance.last_edited_by)
            return instance

        return user(**attrs)


class endpoint_serializer(serializers.ModelSerializer):
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
    enable = serializers.BooleanField()
    description = serializers.CharField(required=False)

    class Meta:
        model = role
        fields = ('pk', 'name', 'enable', 'description')


class role_permission_serializer(serializers.ModelSerializer):
    pk = serializers.Field()
    role = serializers.RelatedField(many=False)
    permission = serializers.RelatedField(many=False)

    class Meta:
        model = role_permission
        fields = ('pk', 'role', 'Permission')


class project_user_role_serializer(serializers.ModelSerializer):
    pk = serializers.Field()
    project = serializers.RelatedField(many=False)
    user = serializers.RelatedField(many=False)
    role = serializers.RelatedField(many=False)

    class Meta:
        model = project_user_role
        fields = ('pk', 'project', 'user', 'role')

