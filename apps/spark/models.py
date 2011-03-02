from django.db import models


class ModelBase(models.Model):
    """
    Base class for models to abstract some common features.
    
    * Adds automatic created and modified fields to the model.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        get_latest_by = 'created'


class Continent(models.Model):
    code = models.CharField(max_length=2, primary_key=True)

    def __unicode__(self):
        return self.name


class Country(models.Model):
    iso = models.CharField(max_length=2, primary_key=True)
    continent = models.ForeignKey(Continent, null=True)

    class Meta:
        ordering = ('iso',)

    def __unicode__(self):
        return self.iso


class City(ModelBase):
    """
    Represents cities used by the global visualization
    """
    country = models.ForeignKey(Country)
    city = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ('country', 'city')
    
    def __unicode__(self):
        return '%s, %s' % (self.country, self.city)
