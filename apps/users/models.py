from django.db import models
from django.contrib.auth.models import User

from tower import ugettext as _
from tower import ugettext_lazy as _lazy

from mptt.models import MPTTModel

from spark.models import City
from challenges.models import Challenge


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    level = models.PositiveIntegerField(default=1)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    city = models.ForeignKey(City, null=True)
    boost1_completed = models.BooleanField(default=False)
    boost2_completed = models.BooleanField(default=False)
    challenges = models.ManyToManyField(Challenge)

    def __unicode__(self):
        return unicode(self.user)
    
    def complete_challenge(challenge):
        """ Forces completion of a challenge. """
        

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


class UserNode(MPTTModel):
    """ 
    Represents a user in the Spark sharing hierarchy.
    This model is mainly used for calculating chains of shares.
    """
    user = models.OneToOneField(User, related_name='node', db_index=True)
    parent = models.ForeignKey('self', default=None, blank=True, null=True,
                                related_name='children')

    class Meta:
        db_table='users_tree'

    class MPTTMeta:
        pass

    def __unicode__(self):
        return unicode(self.user)

