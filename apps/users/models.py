import datetime

from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from tower import ugettext as _, ugettext_lazy as _lazy

from mptt.models import MPTTModel

from spark.urlresolvers import reverse
from spark.helpers import urlparams
from spark.models import City

from sharing import utils as sharing_utils

from challenges.models import Challenge
from challenges import utils


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
    parent_username = models.CharField(max_length=30, blank=True, null=True)
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
        

    def get_absolute_url(self):
        return reverse('desktop.user', args=[self.user.username])
    
    
    @property
    def badges(self):
        """Returns a list of dicts used for badge list rendering.
           They represent all badges earned by the user in the Spark game.
        """
        badges = []
        completed_challenges = CompletedChallenge.objects.filter(profile=self,
                                                                 date_badge_earned__isnull=False)
        for cc in completed_challenges:
            badges.append({
                'id': utils.get_challenge_id(cc.challenge.level, cc.challenge.number),
                'name': cc.challenge.badge_name,
                'description': cc.challenge.badge_description,
                'date_earned': cc.date_badge_earned,
                'new': cc.new_badge
            })
        return badges


    def get_home_location(self, locale):
        """Returns a string containing the location determined by Google Location Services
           when Boost your Spark 1/2 was completed by the user.
        """
        from geo.countries import countries
        if self.country_code and locale in countries:
            country = countries[locale][self.country_code.lower()]
            return '%s, %s' % (self.city_name, country)
        else:
            return ''
    
    
    @property
    def most_recent_share(self):
        """Most recent share stat displayed on desktop dashboard/user pages."""
        from stats.models import SharingHistory
        
        share = SharingHistory.objects.filter(parent=self)[:1]
        if share:
            return share[0].date_shared
        else:
            return None
    
    
    @property
    def shares_over_time(self):
        """Aggregate data of Spark shares since the start of the campaign.
           Used by the 'shares over time' diagram in the user dashboard.
        """
        from stats.models import SharingHistory
        return SharingHistory.get_shares_over_time(self)
    
    
    @property
    def sparked_countries(self):
        """List of countries this user has shared their Spark with."""
        return ['fr', 'br', 'us', 'pt', 'es', 'nz', 'jp', 'kr', 'se', 'ly', 'ro', 'bj', 'in', 'cm', 'ua']
    

    @property
    def longest_chain(self):
        """Longest chain stat displayed on desktop dashboard/user pages."""
        return 0


    @property
    def total_shares(self):
        """Total shares stat displayed on desktop dashboard/user pages."""
        from stats.models import SharingHistory
        
        return SharingHistory.objects.filter(parent=self).count()
    
    
    @property
    def challenge_info(self):
        """Returns a list of dicts containing level/challenge completion information.
           Used to render both desktop and mobile collapsing challenge lists.
        """
        return utils.get_profile_levels(self)


    @property
    def new_challenge_count(self):
        """Returns the number of newly available challenges in the user's current level."""
        if self.new_challenges:
            challenge_count = utils.CHALLENGE_COUNT_PER_LVL[self.level-1]
            completed_challenge_count = len(CompletedChallenge.objects.filter(profile=self,
                                                                              challenge__level=self.level))
            return challenge_count - completed_challenge_count
        else:
            return 0


    @property
    def new_badge_count(self):
        """Returns the number of recently earned badges."""
        return len([b for b in self.badges if b['new']])
    
    
    @property
    def qr_code_download(self):
        """Returns the URL of a QR code which, when scanned, points to: http://[domain]/download?via=qr&user=[username]
        """
        site = Site.objects.get_current()
        url = 'http://%s%s' % (site, urlparams(reverse('sharing.download'), via='qr', user=self.user.username))
        return sharing_utils.url2qr(url)
    
    
    def clear_new_badges(self):
        """Clears notifications of recently earned badges."""
        CompletedChallenge.objects.filter(profile=self, new_badge=True).update(new_badge=False)
    
    
    def clear_new_challenges(self):
        """Clears notifications of new available challenges."""
        self.new_challenges = False
        self.save()


    def complete_challenges(self, challenges):
        """Helper method to easily save the completion of given challenges for this user."""
        error = False
        if challenges:
            for challenge in challenges:
                try:
                    # If the completed challenge is from an upper level and not an easter egg, we keep the badge hidden.
                    # This is done by setting the date_badge_earned to NULL.
                    date = None if self.level < challenge.level and not challenge.easter_egg else datetime.datetime.now()
                
                    CompletedChallenge.objects.create(profile=self, challenge=challenge, date_badge_earned=date, 
                                                      # Don't set new_badge to True if the badge is hidden.
                                                      new_badge=date is not None)
                except IntegrityError:
                    # Challenge was already completed by another concurrent 'update_completed_challenges' task.
                    # In this case, fail silently.
                    pass


# Retrieves or creates a Profile automatically whenever the profile property is accessed
User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])



class CompletedChallenge(models.Model):
    """Mapping table for challenge completion and badge awarding."""
    challenge = models.ForeignKey(Challenge)
    profile = models.ForeignKey(Profile, db_index=True)
    
    date_completed = models.DateTimeField(auto_now_add=True)
    date_badge_earned = models.DateTimeField(blank=True, null=True)
    new_badge = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('challenge', 'profile')
    
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

