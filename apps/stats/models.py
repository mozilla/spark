from django.db import models
from django.contrib.auth.models import User

from spark.models import ModelBase


class PersonalStats(ModelBase):
    user = models.OneToOneField(User, primary_key=True, related_name='stats',
                                verbose_name=_lazy(u'User'))
    longest_chain = models.PositiveIntegerField(default=1,
                                verbose_name=_lazy(u'Longest chain'))
    
    # TODO: other user-specific stats

    def __unicode__(self):
        return unicode(self.user)


class GlobalStats(ModelBase):
    name = models.CharField(verbose_name=_lazy(u('Name')))
    title = models.CharField(blank=True, null=True,
                                verbose_name=_lazy(u'Title'))
    description = models.CharField(blank=True, null=True,
                                verbose_name=_lazy(u'Description'))
    value = models.FloatField(blank=True, null=True,
                                verbose_name=_lazy(u'Value'))
    
    def __unicode__(self):
        return unicode(self.name)