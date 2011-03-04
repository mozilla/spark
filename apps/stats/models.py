from django.db import models
from django.contrib.auth.models import User

from spark.models import ModelBase
from users.models import Profile


class PersonalStats(ModelBase):
    user = models.OneToOneField(User, primary_key=True, related_name='stats')
    longest_chain = models.PositiveIntegerField(default=0)
    total_shares = models.PositiveIntegerField(default=0)
    
    # TODO: other user-specific stats

    def __unicode__(self):
        return unicode(self.user)


class GlobalStats(ModelBase):
    name = models.CharField(primary_key=True)
    value = models.FloatField(blank=True, null=True)
    
    def __unicode__(self):
        return unicode(self.name)


class ShareHistory(ModelBase):
    profile = models.ForeignKey(Profile, db_index=True)
    date_shared = models.DateTimeField(auto_now_add=True)
    shared_via = models.PositiveIntegerField()
    timezone = models.CharField(max_length=6, blank=True, null=True)
    
    def __unicode__(self):
        return '%s at %s via %s' % (profile, date_shared, shared_via)