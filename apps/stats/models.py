from django.db import models

from users.models import Profile
from spark.models import City


class PersonalStats(models.Model):
    user = models.OneToOneField(Profile, primary_key=True,
                                related_name='stats')
    longest_chain = models.PositiveIntegerField(default=0)
    total_shares = models.PositiveIntegerField(default=0)
    
    # TODO: other user-specific stats

    def __unicode__(self):
        return unicode(self.user)



class GlobalStats(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    value = models.FloatField(blank=True, null=True)
    
    def __unicode__(self):
        return unicode(self.name)



VIA_TWITTER = 1
VIA_FACEBOOK = 2
VIA_QR = 3
VIA_POSTER = 4

class SharingHistory(models.Model):
    parent = models.ForeignKey(Profile, db_index=True)
    date_shared = models.DateTimeField(auto_now_add=True)
    shared_via = models.PositiveIntegerField()
    timezone = models.CharField(max_length=6, blank=True, null=True)
    
    class Meta:
        ordering = ('-date_shared',)
    
    def __unicode__(self):
        return '%s on %s' % (profile, shared_via, date_shared)
    
    @classmethod
    def get_num_shares(cls, profile):
        return SharingHistory.objects.filter(parent=profile).count()
    
    @classmethod
    def get_shares_over_time(cls, profile):
        return SharingHistory.objects.filter(parent=profile)
    
    @classmethod
    def add_share(cls, profile):
        SharingHistory.objects.create(parent=profile)
    
    @classmethod
    def add_share_from_twitter(cls, profile):
        SharingHistory.objects.create(parent=profile, shared_via=VIA_TWITTER)

    @classmethod
    def add_share_from_facebook(cls, profile):
        SharingHistory.objects.create(parent=profile, shared_via=VIA_FACEBOOK)

    @classmethod
    def add_share_from_qr_code(cls, profile):
        SharingHistory.objects.create(parent=profile, shared_via=VIA_QR)

    @classmethod
    def add_share_from_poster(cls, profile):
        SharingHistory.objects.create(parent=profile, shared_via=VIA_POSTER)


class CitySharingHistory(models.Model):
    city_from = models.ForeignKey(City, related_name='from_city')
    city_to = models.ForeignKey(City, related_name='to_city')
    sharer = models.ForeignKey(Profile, db_index=True)
    date_shared = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def add_share(cls, from_city, to_city, sharer):
        CitySharingHistory.objects.create(city_from=from_city,
                                          city_to=to_city,
                                          sharer=sharer)
