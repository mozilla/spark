from django.db import models
from django.contrib.auth.models import User

from tower import ugettext as _, ugettext_lazy as _lazy

from mptt.models import MPTTModel

from spark.models import City
from challenges.models import Challenge


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)

    # Game progress
    level = models.PositiveIntegerField(default=1)
    challenges = models.ManyToManyField(Challenge, through='CompletedChallenge')

    # Boost 1/2
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    major_city = models.ForeignKey(City, blank=True, null=True)
    city_name = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    us_state = models.CharField(max_length=2, blank=True, null=True)
    
    # Boost 2/2
    no_parent = models.BooleanField(default=True)
    date_boost2_localtime = models.DateTimeField(blank=True, null=True)
        
    # Flags
    boost1_completed = models.BooleanField(default=False)
    boost2_completed = models.BooleanField(default=False)
    new_challenges = models.BooleanField(default=False)
    login_desktop = models.BooleanField(default=False)
    is_non_android = models.BooleanField(default=False)
    
    # Social sharing
    short_url_twitter = models.CharField(max_length=64, blank=True, null=True)
    short_url_facebook = models.CharField(max_length=64, blank=True, null=True)
    short_url_qr = models.CharField(max_length=64, blank=True, null=True)
    short_url_poster = models.CharField(max_length=64, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.user)

# Retrieves or creates a Profile automatically whenever the profile property is accessed
User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])



class CompletedChallenge(models.Model):
    """Mapping table for challenge completion and badge awarding."""
    challenge = models.ForeignKey(Challenge)
    profile = models.ForeignKey(Profile, db_index=True)
    
    date_completed = models.DateTimeField(auto_now_add=True)
    date_badge_earned = models.DateTimeField(blank=True, null=True)
    new_badge = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s <-> %s" % (profile, challenge)



class UserNode(MPTTModel):
    """ 
    Represents a user in the Spark sharing hierarchy.
    This model is mainly used for storing chains of shares as user trees.
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

