import datetime

from django.db import models
from django.contrib.auth.models import User

from tower import ugettext as _, ugettext_lazy as _lazy

from mptt.models import MPTTModel

from spark.models import City

from challenges.models import Challenge
from challenges.utils import get_profile_levels


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)

    # Game progress
    level = models.PositiveIntegerField(default=1)
    challenges = models.ManyToManyField(Challenge, through='CompletedChallenge')
    new_challenges = models.BooleanField(default=False)
    
    # Boost 1/2
    boost1_completed = models.BooleanField(default=False)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    major_city = models.ForeignKey(City, blank=True, null=True)
    city_name = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    us_state = models.CharField(max_length=2, blank=True, null=True)
    
    # Boost 2/2
    boost2_completed = models.BooleanField(default=False)
    no_parent = models.BooleanField(default=True)
    date_boost2_localtime = models.DateTimeField(blank=True, null=True)

    # Flags
    login_desktop = models.BooleanField(default=False)
    is_non_android = models.BooleanField(default=False)
    
    # Social sharing
    short_url_twitter = models.CharField(max_length=64, blank=True, null=True)
    short_url_facebook = models.CharField(max_length=64, blank=True, null=True)
    short_url_qr = models.CharField(max_length=64, blank=True, null=True)
    short_url_poster = models.CharField(max_length=64, blank=True, null=True)


    def __unicode__(self):
        return unicode(self.user)
    
    
    @property
    def badges(self):
        badges = []
        completed_challenges = CompletedChallenge.objects.filter(profile=self, 
                                                                 date_badge_earned__isnull=False)
        for cc in completed_challenges:
            badges.append({
                'id': '%d_%d' % (cc.challenge.level, cc.challenge.number),
                'name': cc.challenge.badge_name,
                'description': cc.challenge.badge_description,
                'date_earned': cc.date_badge_earned,
                'new': cc.new_badge
            })
        
        return badges
    
    
    @property
    def challenge_info(self):
        return get_profile_levels(self)


    def complete_challenges(self, challenges):
        if challenges:
            for challenge in challenges:
                # If the completed challenge is from an upper level and not an easter egg, we keep the badge hidden.
                # This is done by setting the date_badge_earned to NULL.
                date = None if self.level < challenge.level and not challenge.easter_egg else datetime.datetime.now()
            
                CompletedChallenge.objects.create(profile=self, challenge=challenge, date_badge_earned=date, 
                                                  # Don't set new_badge to True if the badge is hidden.
                                                  new_badge=date is not None)
            self.new_challenges = True
            self.save()


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
        return "%s <-> %s" % (self.profile, self.challenge)



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

