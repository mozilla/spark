from django.db import models

from .utils import challenges, badges, get_challenge_id


class Challenge(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    level = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    easter_egg = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('level', 'number')
    
    def __unicode__(self):
        return get_challenge_id(self.level, self.number)
    
    def get_instructions(self):
        return unicode(challenges[unicode(self)])
    
    def get_badge_name(self):
        return unicode(badges[unicode(self)][0])
    
    def get_badge_description(self):
        return unicode(badges[unicode(self)][1])
