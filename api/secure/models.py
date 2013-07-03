from django.db import models
from django.utils import timezone
from lib import hashtools
from api.auth.models import site_client as site_client_model

class user(models.Model):
	site_client = models.ForeignKey('auth.site_client')
	full_name = models.CharField(max_length=250, db_index=True)
	email_address = models.CharField(max_length=250)
	username = models.CharField(max_length=250, db_index=True, unique=True)
	password = models.CharField(max_length=128)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	disable = models.BooleanField(default=False)
	birthday = models.DateTimeField(null=True)
	avatar = models.ImageField(upload_to='user/avatar', null=True)
	last_login = models.DateTimeField(null=True)
	date_join = models.DateTimeField()
	is_supperuser = models.BooleanField(default=False)
	is_stuff = models.BooleanField(default=False)
	update_time = models.DateTimeField(auto_now_add=True)
	last_edited_by = models.CharField(max_length=250)

	def __unicode__(self):
		return self.username

	class Meta:
		db_table = 'sa_t_user'

	def get_age(self):
		if self.birthday:
			from django.utils.dateparse import parse_datetime
			bd = parse_datetime(str(self.birthday)).replace(tzinfo=None)
			now = timezone.datetime.now().replace(tzinfo=None)
			return (now-bd).days/365
		else:
			return 0

	def get_client_id(self):
		return self.site_client.client_id

	def save(self, *args, **kwargs):
		self.date_join = timezone.now()
		self.full_name = "%s %s" % (self.first_name, self.last_name)
		self.password = hashtools.gen_password(vis_pwd=self.password)
		self.date_join = timezone.now()
			
		self.site_client = site_client_model.objects.get(client_id = self.site_client_id)

		super(user, self).save(*args, **kwargs)


# class AnonymousUser(object):
#     id = None
#     pk = None
#     username = ''
#     is_staff = False
#     is_active = False
#     is_superuser = False
#     _groups = EmptyManager()
#     _user_permissions = EmptyManager()


class endpoint(models.Model):
	name = models.CharField(max_length=100, db_index=True, unique=True)
	codename = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = 'sa_t_endpoint'


class permission(models.Model):
	name = models.CharField(max_length=100, db_index=True, unique=True)
	endpoint = models.ForeignKey("endpoint")
	GPPD = models.SmallIntegerField()

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = 'sa_t_permission'


class role(models.Model):
	name = models.CharField(max_length=100, db_index=True, unique=True)
	description = models.TextField(max_length=10000)

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = 'sa_t_role'


class role_permission(models.Model):
	role = models.ForeignKey('role')
	permission = models.ForeignKey('permission')

	class Meta:
		db_table = 'sa_t_role_permission'


class project_user_role(models.Model):
	project = models.ForeignKey('project.project')
	user = models.ForeignKey('user')
	role = models.ForeignKey('role')

	class Meta:
		db_table = 'sa_t_project_user_role'
