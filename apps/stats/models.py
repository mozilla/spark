from django.db import models

from users.models import Profile
from spark.models import City


class PersonalStats(models.Model):
    user = models.OneToOneField(Profile, primary_key=True, 
                                related_name='stats')
    longest_chain = models.PositiveIntegerField(default=1)
    
    # TODO: other user-specific stats

    def __unicode__(self):
        return unicode(self.user)


class GlobalStats(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    value = models.FloatField(blank=True, null=True)
    
    def __unicode__(self):
        return unicode(self.name)


class SharingHistory(models.Model):
    parent = models.ForeignKey(Profile, db_index=True)
    date_shared = models.DateTimeField(auto_now_add=True)
    shared_via_qr = models.BooleanField(default=False)
    shared_via_poster = models.BooleanField(default=False)
    shared_via_twitter = models.BooleanField(default=False)
    shared_via_facebook = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-date_shared',)
    
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
        SharingHistory.objects.create(parent=profile, shared_via_twitter=True)

    @classmethod
    def add_share_from_facebook(cls, profile):
        SharingHistory.objects.create(parent=profile, shared_via_facebook=True)

    @classmethod
    def add_share_from_qr_code(cls, profile):
        SharingHistory.objects.create(parent=profile, shared_via_qr=True)


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
