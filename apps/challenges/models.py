from django.db import models

from .utils import (get_challenge_id, get_instructions, get_badge_name, 
                    get_badge_description)


class Challenge(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    level = models.PositiveIntegerField(db_index=True)
    number = models.PositiveIntegerField()
    easter_egg = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('level', 'number')
    
    def __unicode__(self):
        return get_challenge_id(self.level, self.number)
    
    @property
    def instructions(self):
        return get_instructions(unicode(self))
    
    @property
    def badge_name(self):
        return get_badge_name(unicode(self))
    
    @property
    def badge_description(self):
        return get_badge_description(unicode(self))