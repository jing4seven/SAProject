from django.db import models
from django.utils import timezone
from django.conf import settings
from api.secure.models import user

class project_manager(models.Manager):
    '''
    Get single project instance by name and owner username.
    '''
    def get_by_natural_key(self, owner_username, project_name):
        owner_id = user.objects.get_by_natural_key(owner_username).pk
        return self.get(**{self.model.PROJECTNAME_FIELD: project_name, self.model.owner: owner_id})

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

    def get_project_roles_by_username(self, username):
        from api.secure.models import project_user_role, user, role
        user_ins = user.objects.get_by_natural_key(username)
        pur_ins_list = project_user_role.objects.filter(project=self, user=user_ins)
        role_list = []
        for pur in pur_ins_list:
            role_list.append(pur.role.name)

        # everybody all has anonymous permissions.
        anon_role_name = role(name=settings.ANONYMOUS_ROLE_NAME)
        role_list.append(anon_role_name)

        return tuple(role_list)

    def get_permissions_by_username(self, username):
        from api.secure.models import project_user_role, user
        user_ins = user.objects.get_by_natural_key(username)
        pur_ins_list = project_user_role.objects.filter(project=self, user=user_ins)
        perm_list = []
        for pur in pur_ins_list:
            perm_list.append(pur.Permission)

        pur_ins_list = self.get_anonymous_permissions()
        for pur in pur_ins_list:
            perm_list.append(pur.Permission)

        return tuple(set(perm_list))

    def get_anonymous_permissions(self):
        from api.secure.models import project_user_role, user,role
        # everybody all has anonymous permissions.
        anon_role_name = role(name=settings.ANONYMOUS_ROLE_NAME)
        user_ins = user.objects.get_by_natural_key(anon_role_name)
        pur_ins_list = project_user_role.objects.filter(project=self, user=user_ins)
        return pur_ins_list


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


# class work_item_group(models.Model):
#     project = models.ForeignKey('project')
#     name = models.CharField("work item group name", max_length=50)
#     parent = models.ForeignKey('self', null=True)
#     description = models.TextField(blank=True, null=True)
#     importance = models.PositiveSmallIntegerField(blank=True, default=0)
#     time_logged = models.PositiveIntegerField(blank=True, default=0)
#     initial_estimate = models.PositiveIntegerField(blank=True)
#     how_to_demo = models.TextField()
#     update_time = models.DateTimeField(default=timezone.now(), blank=True)
#     last_eidted_by = models.CharField(max_length=250, blank=True)
#
#     def __unicode__(self):
#         return self.name
#
#     class Meta:
#         db_table = 'sa_t_work_item_groups'


# class work_item_group_hierachy(models.Model):
#     parent = models.ForeignKey(work_item_group, related_name="parent", null=True)
#     childs = models.ForeignKey(work_item_group, related_name="childs", blank=True, null=True)

#     class Meta:
#         #unique_together = (("parent", "childs"),)
#         db_table = 'sa_t_work_item_group_hierachy'

# class work_item_status(models.Model):
#     name = name = models.CharField(max_length=50)
#     description = models.TextField(blank=True, null=True)
#     creator = models.ForeignKey('secure.user', null=True)


# class work_item(models.Model):
#     id = PositiveBigIntegerAutoField(primary_key=True)
#     work_item_group = models.ForeignKey('work_item_group')
#     release = models.ForeignKey('release', null=True)
#     status = models.ForeignKey('work_item_status')
#     name = models.CharField(max_length=250)
#     description = models.TextField(blank=True, null=True)
#     LoE = models.PositiveIntegerField(blank=True, null=True)
#     creator = models.ForeignKey('secure.user', related_name="creator")
#     assignee = models.ForeignKey('secure.user', related_name="assignee")
#     requestor = models.ForeignKey('secure.user', related_name="requestor")
#     time_logged = models.PositiveIntegerField(null=True, blank=True)
#     update_time = models.DateTimeField(default=timezone.now(), blank=True)
#     last_eidted_by = models.CharField(max_length=250, blank=True)

#     def __unicode__(self):
#         return self.name

#     class Meta:
#         db_table = 'sa_t_work_items'

