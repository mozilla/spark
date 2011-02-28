from django.db import models
from django.contrib.auth.models import User

from spark.models import ModelBase


class PersonalStats(ModelBase):
    user = models.OneToOneField(User, primary_key=True, related_name='stats')
    longest_chain = models.PositiveIntegerField(default=1)
    
    # TODO: other user-specific stats

    def __unicode__(self):
        return unicode(self.user)


class GlobalStats(ModelBase):
    name = models.CharField(primary_key=True)
    value = models.FloatField(blank=True, null=True)
    
    def __unicode__(self):
        return unicode(self.name)