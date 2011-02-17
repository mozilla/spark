from django.db import models
from django.contrib.auth.models import User

from tower import ugettext as _
from tower import ugettext_lazy as _lazy

from mptt.models import MPTTModel

from spark.models import City


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True,
                                verbose_name=_lazy(u'User'))
    level = models.PositiveIntegerField(default=1,
                                verbose_name=_lazy(u'Level'))
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    city = models.ForeignKey(City, null=True)

    def __unicode__(self):
        return unicode(self.user)


class UserNode(MPTTModel):
    """ 
    Represents a user in the Spark sharing hierarchy.
    This model is mainly used for calculating chains of shares.
    """
    user = models.OneToOneField(User, related_name='node',
                                verbose_name=_lazy(u'User'))
    parent = models.ForeignKey('self', default=None, blank=True, null=True,
                                related_name='children')

    class Meta:
        db_table='users_tree'

    class MPTTMeta:
        pass

    def __unicode__(self):
        return unicode(self.user)
