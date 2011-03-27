from datetime import datetime, timedelta

from django.conf import settings
from django.db import models, IntegrityError
from django.db.models import Count

from users.models import Profile
from spark.models import City

from geo.continents import countries_continents




class GlobalStats(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    value = models.PositiveIntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return unicode(self.name)
    
    @classmethod
    def increment_total_sparks(cls):
        try:
            stat = GlobalStats.objects.get(name='total_sparks')
            stat.value += 1
            stat.save()
        except GlobalStats.DoesNotExist:
            pass
    
    @classmethod
    def increment_total_badges(cls):
        try:
            stat = GlobalStats.objects.get(name='total_badges')
            stat.value += 1
            stat.save()
        except GlobalStats.DoesNotExist:
            pass
            
    @classmethod
    def get_total_sparks(cls):
        try:
            stat = GlobalStats.objects.get(name='total_sparks')
            return stat.value
        except GlobalStats.DoesNotExist:
            return 0

    @classmethod
    def get_total_badges(cls):
        try:
            stat = GlobalStats.objects.get(name='total_badges')
            return stat.value
        except GlobalStats.DoesNotExist:
            return 0


class ContinentSparked(models.Model):
    continent_code = models.CharField(max_length=2, primary_key=True)

    def __unicode__(self):
        return unicode(self.continent_code)

    @classmethod
    def get_total_continents_sparked(cls):
        return ContinentSparked.objects.count()

    @classmethod
    def add_continent(cls, continent_code):
        try:
            ContinentSparked.objects.create(continent_code=continent_code)
        except IntegrityError:
            # Ignore already sparked continents
            pass


class CountrySparked(models.Model):
    country_code = models.CharField(max_length=2, primary_key=True)

    def __unicode__(self):
        return unicode(self.country_code)

    @classmethod
    def get_total_countries_sparked(cls):
        return CountrySparked.objects.count()

    @classmethod
    def add_country(cls, country_code):
        try:
            CountrySparked.objects.create(country_code=country_code)
            
            try:
                continent_code = countries_continents[country_code]
                ContinentSparked.add_continent(continent_code)
            except KeyError:
                pass
        except IntegrityError:
            # Ignore already sparked countries
            pass



VIA_TWITTER = 1
VIA_FACEBOOK = 2
VIA_QR = 3
VIA_POSTER = 4
UNKNOWN = 5

class SharingHistory(models.Model):
    parent = models.ForeignKey(Profile, db_index=True)
    date_shared = models.DateTimeField(auto_now_add=True)
    shared_via = models.PositiveIntegerField(default=UNKNOWN)
    timezone = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('-date_shared',)

    def __unicode__(self):
        return '%s via %s' % (self.parent, self.shared_via)

    @classmethod
    def get_num_shares(cls, profile):
        return SharingHistory.objects.filter(parent=profile).count()
    
    @classmethod
    def get_max_share_count(cls):
        shares = SharingHistory.objects.values('parent').annotate(num_shares=Count('parent')).order_by('-num_shares')
        if shares:
            return shares[0]['num_shares']
        return 0

    @classmethod
    def get_shares_over_time(cls, profile):
        start = settings.CAMPAIGN_STARTING_DATE - timedelta(days=1)
        num_days = (datetime.now() + timedelta(days=1) - start).days
        shares = [0 for i in range(num_days)]
        date_range = (start + timedelta(days=i) for i in range(num_days))
        dates = [(i, '%d-%d' % (d.day, d.month)) for (i, d) in enumerate(date_range)]
        
        qs = (SharingHistory.objects.filter(parent=profile)
                           .extra(select={'month': 'extract(month from date_shared)', 
                                          'day': 'extract(day from date_shared)'})
                            .values('month', 'day').annotate(num_shares=Count('date_shared')))
        
        for r in qs:
            day = '%d-%d' % (r['day'], r['month'])
            for (i, date) in dates:
                if date == day:
                    shares[i] = r['num_shares']
                    break
        
        return shares
    
    @classmethod
    def has_gained_shares_via(cls, profile, service):
        return SharingHistory.objects.filter(parent=profile, shared_via=service).count() >= 1
        
    @classmethod
    def add_share(cls, profile, tz_offset=None):
        SharingHistory.objects.create(parent=profile, timezone=tz_offset)

    @classmethod
    def add_share_from_twitter(cls, profile, tz_offset=None):
        SharingHistory.objects.create(parent=profile, shared_via=VIA_TWITTER, timezone=tz_offset)

    @classmethod
    def add_share_from_facebook(cls, profile, tz_offset=None):
        SharingHistory.objects.create(parent=profile, shared_via=VIA_FACEBOOK, timezone=tz_offset)

    @classmethod
    def add_share_from_qr_code(cls, profile, tz_offset=None):
        SharingHistory.objects.create(parent=profile, shared_via=VIA_QR, timezone=tz_offset)

    @classmethod
    def add_share_from_poster(cls, profile, tz_offset=None):
        SharingHistory.objects.create(parent=profile, shared_via=VIA_POSTER, timezone=tz_offset)
    
    @property
    def local_hour(self):
        """Returns the hour at which the visitor triggered the share (local time).
           This is needed by challenges like "Share with someone between 6am and 10am".
        """
        if self.timezone:
            PDT_offset = timedelta(hours=7)
            visitor_utc_offset = timedelta(hours=-self.timezone)
            local_dt = self.date_shared + PDT_offset + visitor_utc_offset
        
            return local_dt.hour
        else:
            return None


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

    @classmethod
    def add_share_from_profiles(cls, sharer, sharee):
        from .tasks import get_ordered_cities
        
        city1 = sharer.major_city
        city2 = sharee.major_city
        
        if city1 and city2:
            city_positions = get_ordered_cities()

            # City pairs are sorted by longitude in CitySharingHistory
            if city_positions[city1.id] < city_positions[city2.id]:
                CitySharingHistory.add_share(city1, city2, sharer)
            else:
                CitySharingHistory.add_share(city2, city1, sharer)
