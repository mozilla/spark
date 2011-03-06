from django.db import models

from geo.countries import countries


class City(models.Model):
    """
    Represents cities used by the global visualization.
    """
    name = models.CharField(max_length=255, primary_key=True)
    country_code = models.CharField(max_length=2)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __unicode__(self):
        return '%s, %s' % (self.name, self.country_code)
    
    @property
    def country(self):
        return unicode(countries[self.country_code])