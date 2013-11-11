from django.db import models
from django.utils import timezone
from django.conf import settings
from api.secure.models import user

class project_manager(models.Manager):
    '''
    Get single project instance by name and owner username.
    '''
    def get_by_natural_key(self, owner_username, project_name):
        owner = user.objects.get_by_natural_key(owner_username)
        return self.get(name=project_name, owner=owner)

    def get_team_members(self):
        from api.secure.models import project_user_role
        pur_ins_list = project_user_role.objects.filter(project=self)
        user_list = []
        for pur in pur_ins_list:
            user_list.append(pur.user)

        return tuple(user_list)

    def get_team_members_username(self):
        user_list = self.get_team_members()
        username_list = []
        for user in user_list:
            username_list.append(user.username)

        return tuple(username_list)


class project(models.Model):
    name = models.CharField("project short name use for navigation", max_length=50)
    alias = models.CharField("full name of project", max_length=250)
    owner = models.ForeignKey(user)
    description = models.TextField(blank=True, null=True)
    is_private = models.BooleanField("private project only visible for owner and memebers of his/her group.", blank=True)
    update_time = models.DateTimeField(default=timezone.now(), blank=True)
    last_edited_by = models.CharField(max_length=250, blank=True)

    objects = project_manager()

    PROJECTNAME_FIELD = 'name'

    def __unicode__(self):
        return self.alias

    class Meta:
        db_table = 'sa_t_projects'


class project_status(models.Model):
    name = models.CharField("status name of project", max_length=50)
    project = models.ForeignKey(project, blank=True)
    is_current = models.BooleanField("the project current status or not", default=False)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'sa_t_project_status'

class release(models.Model):
    name = models.CharField('release name', max_length=250)
    project = models.ForeignKey(project, blank=False)
    description = models.TextField('description of the release', blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(default=timezone.now(), blank=True)
    last_edited_by = models.CharField(max_length=250, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'sa_t_releases'

class release_status(models.Model):
    name = models.CharField('release status name', max_length=50)
    description = models.TextField(blank=True, null=True)
    release = models.ForeignKey(release, blank=True)
    is_current = models.BooleanField('the release current status or not', default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'sa_t_release_status'


class work_item_group(models.Model):
    project = models.ForeignKey(project, blank=False)
    parent = models.ForeignKey('self', null=True)
    name = models.CharField('name of the work item group', max_length=250)
    description = models.TextField(blank=True, null=True)
    importance = models.SmallIntegerField(default=0)
    time_logged = models.IntegerField(default=0)
    initial_estimate = models.IntegerField(default=0)
    #how_to_demo = models.BigIntegerField(default=0)
    update_time = models.DateTimeField(default=timezone.now(), blank=True)
    last_edited_by = models.CharField(max_length=250, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'sa_t_work_item_groups'


class work_item(models.Model):
    work_item_group = models.ForeignKey(work_item_group, blank=False)
    release = models.ForeignKey(release, blank=True, null=True)
    parent = models.ForeignKey('self', null=True)
    name = models.CharField(max_length=250, blank=False)
    description = models.TextField(blank=True, null=True)
    loe = models.IntegerField(default=0)
    creator = models.ForeignKey(user, blank=False, null=False, related_name='creator_user_relationship')
    assignee = models.ForeignKey(user, blank=True, null=True, related_name='assignee_user_relationship')
    requestor = models.ForeignKey(user, blank=True, null=True, related_name='requestor_user_relationship')
    time_logged = models.IntegerField(default=0)
    update_time = models.DateTimeField(default=timezone.now(), blank=True)
    last_edited_by = models.CharField(max_length=250, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'sa_t_work_items'

