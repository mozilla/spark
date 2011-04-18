import datetime

from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse as django_reverse
from django.utils.http import urlquote
from django.conf import settings

from tower import ugettext as _, ugettext_lazy as _lazy

from mptt.models import MPTTModel

from spark.urlresolvers import reverse, absolute_url
from spark.helpers import urlparams
from spark.models import City

from sharing import utils as sharing_utils
from sharing.messages import TWITTER_BADGE_MSG, FACEBOOK_BADGE_MSG

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
    login_mobile = models.BooleanField(default=False)
    is_non_android = models.BooleanField(default=False)
    
    # Personal stats
    longest_chain = models.PositiveIntegerField(default=0)


    def __unicode__(self):
        return unicode(self.user)
        

    def get_absolute_url(self):
        return reverse('desktop.user', args=[self.user.username])


    @property
    def generic_sharing_url(self):
        url = urlparams(django_reverse('desktop.user', args=[self.user.username]))
        return absolute_url(url)
        
    
    def _social_sharing_url(self, service):
        # django_reverse used instead of reverse because we don't want a locale preprended to sharing links.
        url = urlparams(django_reverse('desktop.user', args=[self.user.username]), 
                                                                f=service)
        return absolute_url(url)


    @property
    def twitter_sharing_url(self):
        return self._social_sharing_url('t')


    @property
    def facebook_sharing_url(self):
        return self._social_sharing_url('fb')


    @property
    def poster_sharing_url(self):
        return self._social_sharing_url('p')


    @property
    def badges(self):
        """Returns a list of dicts used for badge list rendering.
           They represent all badges earned by the user in the Spark game.
        """
        badges = []
        completed_challenges = CompletedChallenge.objects.filter(profile=self,
                                                                 date_badge_earned__isnull=False)
        for cc in completed_challenges:
            badge_id = utils.get_challenge_id(cc.challenge.level, cc.challenge.number)
            badge_description = cc.challenge.badge_description
            badges.append({
                'id': badge_id,
                'name': cc.challenge.badge_name,
                'description': badge_description,
                'date_earned': cc.date_badge_earned,
                'new': cc.new_badge,
                'twitter_msg': urlquote(unicode(TWITTER_BADGE_MSG % {'badge_name':cc.challenge.badge_name, 'short_url':''})),
                'facebook_msg': urlquote(unicode(FACEBOOK_BADGE_MSG % {'badge_name':cc.challenge.badge_name})),
                'facebook_img': absolute_url(settings.MEDIA_URL+'img/badges/fb/'+badge_id.replace('_','-')+'.png'),
                'facebook_desc': urlquote(badge_description)
            })
        return badges
    
    
    def has_badge(self, badge_id):
        """Returns whether this user has earned the given badge."""
        if badge_id:
            return CompletedChallenge.objects.filter(profile=self, challenge__pk=badge_id,
                                                date_badge_earned__isnull=False).count() == 1
        else:
            return False


    @property
    def total_badges_earned(self):
        """Returns the total number of badges earned by the user.
           Doesn't include hidden unlocked badges from an upper level.
        """
        return CompletedChallenge.objects.filter(profile=self, date_badge_earned__isnull=False).count()


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
    def spark_started_with(self):
        if self.parent_username is not None:
            return self.parent_username
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
        from .utils import user_node

        countries = set()
        node = user_node(self.user)
        for child in node.get_children():
            cc = child.user.profile.country_code
            if cc:
                countries.add(cc.lower())
        
        return list(countries)


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
        """Returns the URL of a QR code which, when scanned, points to: https://[domain]/download?f=qr&user=[username]
        """
        url = absolute_url(urlparams(django_reverse('sharing.download'), user=self.user.username))
        return sharing_utils.url2qr(url)
    
    
    @property
    def continent_code(self):
        from geo.continents import countries_continents
        code = ''
        if self.country_code:
            code = countries_continents[self.country_code]
        
        return code


    @property
    def total_countries_sparked(self):
        """Returns the total number of countries where the user's children are located."""
        return len(self.sparked_countries)

    
    @property
    def total_continents_sparked(self):
        """Returns the total number of continents where the user's children are located."""
        from geo.continents import countries_continents
        from .utils import user_node
        
        continents = set()
        node = user_node(self.user)
        for child in node.get_children():
            cc = child.user.profile.country_code
            if cc:
                continents.add(countries_continents[cc])
        return len(continents)
    
    
    @property
    def children_profiles(self):
        """Returns a list of profiles of the user's children in the user tree."""
        from .utils import user_node
        
        return [child.user.profile for child in user_node(self.user).get_children()]
    
    
    def clear_new_badges(self):
        """Clears notifications of recently earned badges."""
        CompletedChallenge.objects.filter(profile=self, new_badge=True).update(new_badge=False)
    
    
    def clear_new_challenges(self):
        """Clears notifications of new available challenges."""
        self.new_challenges = False
        self.save()


    def complete_challenges(self, challenges):
        """Helper method to easily save the completion of given challenges for this user."""
        from stats.models import GlobalStats
        
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

                    GlobalStats.increment_total_badges()
                        
                except IntegrityError:
                    # Challenge was already completed by another concurrent 'update_completed_challenges' task.
                    # In this case, fail silently.
                    pass
    
    
    def trigger_multisparker_badge(self):
        from challenges.tasks import update_completed_challenges
        
        if self.login_desktop and self.login_mobile:
            update_completed_challenges(self.user.id)
    
    
    def update_ancestors_longest_chain(self):
        """Updates 'longest chain' stat of all ancestors of this user when relevant.
           Used after Boost step 2 confirmation so that all users involved have their longest chain stat updated.
        """
        from .utils import user_node

        ancestors = user_node(self.user).get_ancestors()
        chain_length = len(ancestors)
        
        for profile in (ancestor.user.profile for ancestor in ancestors):
            if profile.longest_chain < chain_length:
                profile.longest_chain = chain_length
                profile.save()
            chain_length -= 1


    def add_city_shares_for_children(self):
        """Creates city shares in the CitySharingHistory for the global visualization.
           This is useful when a user already has children when he completes boost 1 (geolocation).
           As soon as it's completed, city shares are created for all geolocated children.
        """
        from stats.models import CitySharingHistory
        
        for child in self.children_profiles:
            if child.boost1_completed:
                CitySharingHistory.add_share_from_profiles(self, child)


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

