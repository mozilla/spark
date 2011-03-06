from spark.tests import TestCase
from nose.tools import eq_

from users.models import User, CompletedChallenge

from challenges.models import Challenge
from challenges.utils import award_hidden_badges


class AwardHiddenBadges(TestCase):
    fixtures = ['boost.json', 'challenges.json', 'completed_challenges.json']
    
    def setUp(self):
        self.profile = User.objects.create(username='test_user').profile
    
    def get_hidden_badges(self):
        return CompletedChallenge.objects.filter(profile=self.profile, 
                                                 date_badge_earned=None)
    
    def test_new_level_awards_hidden_badges(self):
        eq_(1, self.profile.level)
        self.profile.complete_challenges(Challenge.objects.filter(pk__in=['2_1', '2_2']))
        
        eq_(2, len(self.get_hidden_badges()))
        
        # Fake gaining a new level
        self.profile.level = 2
        award_hidden_badges(self.profile)
        eq_(0, len(self.get_hidden_badges()))
        

    def test_awarding_badges_sets_new_badge_flag(self):
        challenge = Challenge.objects.get(pk='2_1')
        self.profile.complete_challenges([challenge])
        
        eq_(False, self.get_hidden_badges()[0].new_badge)
        
        self.profile.level = 2
        award_hidden_badges(self.profile)
        
        eq_(True, CompletedChallenge.objects.get(profile=self.profile,
                                                 challenge=challenge).new_badge)