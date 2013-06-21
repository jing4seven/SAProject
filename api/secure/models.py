from django.db import models
from lib.model import PositiveBigIntegerAutoField
from django.core.files import images

class user(models.Model):
	id = PositiveBigIntegerAutoField(primary_key=True)
	full_name = models.CharField(max_length=250)
	email_address = models.CharField(max_length=250)
	username = models.CharField(max_length=250)
	password = models.CharField(max_length=128)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	disable = models.BooleanField(default=False)
	birthday = models.DateTimeField(null=True)
	avatar = models.ImageField(upload_to='user/avatar', null=True)
	last_login = models.DateTimeField()
	date_join = models.DateTimeField()
	is_supperuser = models.BooleanField(default=False)
	is_stuff = models.BooleanField(default=False)
	update_time = models.DateTimeField(auto_now_add=True)
	last_edited_by = models.CharField("static username", max_length=250)

	def __unicode__(self):
		return self.username

	class Meta:
		db_table = 'sa_t_user'

class content_type(models.Model):
	name = models.CharField(max_length=100)
	app_label = models.CharField(max_length=100)
	model = models.CharField(max_length=100)

	def __unicode__(self):
		return self.pk + "_" + self.name

class permission(models.Model):
	name = models.CharField(max_length=100)
	content_type = models.ForeignKey(content_type)
	code_name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.pk + "_" + self.name

	class Meta:
		db_table = 'sa_t_permission'

class user_permission(models.Model):
	user = models.ForeignKey(user)
	permission = models.ForeignKey(permission)

	class Meta:
		db_table = 'sa_t_user_permission'

class role(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(max_length=10000)

	class Meta:
		db_table = 'sa_t_role'

class user_role(models.Model):
	user = models.ForeignKey(user)
	role = models.ForeignKey(role)

	class Meta:
		db_table = 'sa_t_user_role'

class role_permission(models.Model):
	role = models.ForeignKey(role)
	permission = models.ForeignKey(permission)

	class Meta:
		db_table = 'sa_t_role_permission'
