from django.db import models

from .challenges import challenges
from .badges import badges


class Challenge(models.Model):
    level = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    easter_egg = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('level', 'number')
    
    def __unicode__(self):
        if self.level == 6:
            return 'ee_ch%d' % self.number
        else:
            return 'lvl%d_ch%d' % (self.level, self.number)
    
    def get_instructions(self):
        return unicode(challenges[unicode(self)])
    
    def get_badge_name(self):
        return unicode(badges[unicode(self)][0])
    
    def get_badge_description(self):
        return unicode(badges[unicode(self)][1])
    
    