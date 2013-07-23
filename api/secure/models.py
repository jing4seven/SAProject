from __future__ import unicode_literals
import re
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.db.models.manager import EmptyManager
from django.utils.crypto import get_random_string
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)
from django.conf import settings
from django.utils.decorators import classonlymethod


class SiteProfileNotAvailable(Exception):
    pass

class BaseUserManager(models.Manager):

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def make_random_password(self, length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        """
        Generates a random password with the given length and given
        allowed_chars. Note that the default value of allowed_chars does not
        have "I" or "O" or letters and digits that look similar -- just to
        avoid confusion.
        """
        return get_random_string(length, allowed_chars)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})



class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = UserManager.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        u = self.create_user(username, email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


@python_2_unicode_compatible
class AbstractBaseUser(models.Model):
    password = models.CharField(_('password'), max_length=128)
    last_login = models.DateTimeField(_('last login'), default=timezone.now)

    is_active = True

    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def get_full_name(self):
        raise NotImplementedError()

    def get_short_name(self):
        raise NotImplementedError()


class PermissionMixin(object):
    '''
    Permission related fields in saproject.
    '''
    def get_anonymous_permissions(self):
        '''
        Return default anonymous permissions.
        '''
        pass

    def get_permissions(self,owner_username, project_name=None):
        '''
        Get a list shows permissions that current user has permission to access.
        '''
        if not project_name:
            return self.get_anonymous_permissions()

        #from api.project.models import project as project_model
        #proj_ins = project_model.objects.get(name=prooject_name, owner_username)
        #u_ins = user.objects.get(username=self.username)


    def has_permission(self, project_name=None, view_namespace=None, http_method=None):
        '''
        Check if current user has permission to access specified view with given http method.

        Return `True` if pass, otherwise return `False`.
        '''
        pass


class AbstractUser(AbstractBaseUser, PermissionMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_superuser = False
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_absolute_url(self):
        return "/user/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_age(self):
        if self.birthday:
            from django.utils.dateparse import parse_datetime
            bd = parse_datetime(str(self.birthday)).replace(tzinfo=None)
            now = timezone.datetime.now().replace(tzinfo=None)
            return (now-bd).days/365
        else:
            return 0


class user(AbstractUser):
    """
    Users within the saproject authentication system are represented by this
    model.

    Username, password and email are required. Other fields are optional.
    """
    site_client = models.ForeignKey('auth.site_client')
    #avatar = models.ImageField(upload_to='user/avatar', null=True)
    update_time = models.DateTimeField(auto_now_add=True)
    last_edited_by = models.CharField(max_length=250)
    birthday = models.DateTimeField(null=True)

    class Meta:
        db_table = 'sa_t_user'
        #swappable = 'AUTH_USER_MODEL'


class AnonymousUser(object):
    id = None
    pk = None
    username = ''
    is_staff = False
    is_active = False
    is_superuser = False
    _user_permissions = EmptyManager()


class endpoint(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)
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

    def get_anonymous_permissions(self):
        from api.secure.models import role_permission, role
        # everybody all has anonymous permissions.
        anon_role = role(name=settings.ANONYMOUS_ROLE_NAME)
        rp_ins_list = role_permission.objects.filter(role=anon_role)
        perm_list = []
        for rp in rp_ins_list:
            perm_list.append(rp.permission)

        return self.__get_permissions_by_perm_ins(perm_list)

    def __get_permissions_by_perm_ins(self, perm_ins_list):
        result_list = []
        for perm in perm_ins_list:
            temp_dict = dict()
            temp_dict['codename'] = perm.endpoint.codename
            temp_dict['GPPD'] = perm.GPPD
            result_list.append(temp_dict)

        return tuple(set(result_list))


#class role_manager(models.Manager):

    #@classonlymethod
    #def get_anonymous_role():
        #anon_role_name = settings.ANONYMOUS_ROLE_NAME
        #role_ins = role.objects.get(name=anon_role_name)
        #return role_ins

class role(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    enable = models.BooleanField(default=True)
    description = models.TextField(max_length=10000)

    def __unicode__(self):
        return self.name

    @classonlymethod
    def get_anonymous_role():
        anon_role_name = settings.ANONYMOUS_ROLE_NAME
        return role.objects.get(name=anon_role_name)

    class Meta:
        db_table = 'sa_t_role'


class role_permission(models.Model):
    role = models.ForeignKey('role')
    permission = models.ForeignKey('permission')

    class Meta:
        db_table = 'sa_t_role_permission'

    def get_anonymous_role_name(self):
        return 'AYS'


class project_user_role(models.Model):
    project = models.ForeignKey('project.project')
    user = models.ForeignKey('user')
    role = models.ForeignKey('role')

    class Meta:
        db_table = 'sa_t_project_user_role'
