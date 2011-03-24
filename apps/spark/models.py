from django.db import models

from geo.countries import countries
from geo.cities import cities


class City(models.Model):
    """
    Represents major cities used by the global visualization.
    """
    city_name = models.CharField(max_length=255, unique=True, db_index=True)
    country_code = models.CharField(max_length=2)
    latitude = models.FloatField()
    longitude = models.FloatField(db_index=True)
    is_capital = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-longitude',)
        
    
    def __unicode__(self):
        return '%s, %s' % (self.city_name, self.country_code)
    
    def get_country_name(self, locale):
        if not locale in countries:
            locale = 'en-US'
        return countries[locale][self.country_code.lower()]
    
    @property
    def name(self):
        return unicode(cities[self.city_name]['name'])