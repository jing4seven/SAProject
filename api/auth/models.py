from django.db import models
from django.utils.http import urlquote
from lib import hashtools


class site_client(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True, default="")
    client_id = models.CharField(max_length=255, db_index=True, unique=True)
    security_key = models.CharField(max_length=255, db_index=True, unique=True)
    scope = models.CharField(max_length=255, db_index=True, null=True)
    enable = models.BooleanField(default=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('created_time',)
        db_table = 'sa_t_site_client'

    def save(self, *args, **kwargs):
        c_id = hashtools.gen_random_key()
        self.client_id = c_id
        self.security_key = hashtools.gen_random_key_by_given_key(c_id)

        super(site_client, self).save(*args, **kwargs)
