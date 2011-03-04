from challenges.tasks import update_completed_challenges, _update_level

from spark.tests import TestCase
from nose.tools import eq_

from users.models import User

from challenges.models import Challenge


class UpdateCompletedChallenges(TestCase):
    fixtures = ['boost.json', 'challenges.json']
    
    def test_complete_3_challenges(self):
        profile = User.objects.get(username='franck').profile
        
        eq_(0, profile.challenges.count())
        eq_(1, profile.level)
        
        update_completed_challenges(profile)
        
        # This user has completed both Boost steps.
        # Should complete challenges: 1_2, 1_3
        eq_(2, profile.challenges.count())
        eq_(["1_2", "1_3"], [unicode(c) for c in profile.challenges.all()])


class UpdateLevel(TestCase):
    fixtures = ['challenges.json']
    
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user.save()
        self.profile = self.user.profile
    
    def test_complete_level_1(self):
        eq_(1, self.profile.level)
        
        self.profile.challenges.add(Challenge.objects.get(pk='1_2'))
        _update_level(self.profile)
        
        eq_(2, self.profile.level)
    
    def test_complete_level_2(self):
        self.profile.level = 2
        # Fake completion of four challenges from level 2
        self.profile.challenges = Challenge.objects.filter(pk__in=['2_1', '2_3', '2_6', '2_7'])
        _update_level(self.profile)

        eq_(3, self.profile.level)
        
    def test_complete_level_3(self):
        self.profile.level = 3
        # Fake completion of four challenges from level 3
        self.profile.challenges = Challenge.objects.filter(pk__in=['3_1', '3_2', '3_4', '3_6'])
        _update_level(self.profile)

        eq_(4, self.profile.level)

    def test_complete_level_4(self):
        self.profile.level = 4
        # Fake completion of all challenges in level 4 and previous levels
        self.profile.challenges = Challenge.objects.filter(level__lt=5)
        _update_level(self.profile)

        eq_(5, self.profile.level)
    
    def test_gain_multiple_levels(self):
        self.profile.level = 1
        # Fake completion of all challenges in level 1 and 2
        self.profile.challenges = Challenge.objects.filter(level__lt=3)
        _update_level(self.profile)

        eq_(3, self.profile.level)


