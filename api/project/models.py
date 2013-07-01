from django.db import models
from django.utils import timezone

from api.secure.models import user


class project(models.Model):
	name = models.CharField("project short name use for navigation", max_length=50)
	alias = models.CharField("full name of project", max_length=250)
	owner = models.ForeignKey(user)
	description = models.TextField(blank=True, null=True)	
	is_private = models.BooleanField("private project only visible for owner and memebers of his/her group.", blank=True)
	update_time = models.DateTimeField(default=timezone.now(), blank=True)
	last_edited_by = models.CharField(max_length=250, blank=True)

	def __unicode__(self):
		return self.alias

	class Meta:
		db_table = 'sa_t_project'


class project_status(models.Model):
	name = models.CharField("status name of project", max_length=50)
	project = models.ForeignKey(project, blank=True)
	is_current = models.BooleanField("the project current status or not", default=False)
	description = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = 'sa_t_project_status'



class work_item_group(models.Model):
	project = models.ForeignKey('project')
	name = models.CharField("work item group name", max_length=50)
	parent = models.ForeignKey('self', null=True)
	description = models.TextField(blank=True, null=True)
	importance = models.PositiveSmallIntegerField(blank=True, default=0)
	time_logged = models.PositiveIntegerField(blank=True, default=0)
	initial_estimate = models.PositiveIntegerField(blank=True)
	how_to_demo = models.TextField()
	update_time = models.DateTimeField(default=timezone.now(), blank=True)
	last_eidted_by = models.CharField(max_length=250, blank=True)

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = 'sa_t_work_item_groups'


# class work_item_group_hierachy(models.Model):
# 	parent = models.ForeignKey(work_item_group, related_name="parent", null=True)
# 	childs = models.ForeignKey(work_item_group, related_name="childs", blank=True, null=True)

# 	class Meta:
# 		#unique_together = (("parent", "childs"),)
# 		db_table = 'sa_t_work_item_group_hierachy'

class work_item_status(models.Model):
	name = name = models.CharField(max_length=50)
	description = models.TextField(blank=True, null=True)
	creator = models.ForeignKey('secure.user', null=True)


# class work_item(models.Model):
# 	id = PositiveBigIntegerAutoField(primary_key=True)
# 	work_item_group = models.ForeignKey('work_item_group')
# 	release = models.ForeignKey('release', null=True)
# 	status = models.ForeignKey('work_item_status')
# 	name = models.CharField(max_length=250)
# 	description = models.TextField(blank=True, null=True)
# 	LoE = models.PositiveIntegerField(blank=True, null=True)
# 	creator = models.ForeignKey('secure.user', related_name="creator")
# 	assignee = models.ForeignKey('secure.user', related_name="assignee")
# 	requestor = models.ForeignKey('secure.user', related_name="requestor")
# 	time_logged = models.PositiveIntegerField(null=True, blank=True)
# 	update_time = models.DateTimeField(default=timezone.now(), blank=True)
# 	last_eidted_by = models.CharField(max_length=250, blank=True)

# 	def __unicode__(self):
# 		return self.name

# 	class Meta:
# 		db_table = 'sa_t_work_items'

