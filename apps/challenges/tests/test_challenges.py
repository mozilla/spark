import logging

from spark.tests import TestCase
from nose.tools import eq_

from users.models import User

from challenges.challenges import all_challenges


class ChallengesTestCase(TestCase):
    fixtures = ['boost.json', 'challenges.json']

    def get_profile(self, username):
        return User.objects.get(username=username).profile

        
    def assert_completion(self, profile, challenge_id): 
        eq_(True, all_challenges[challenge_id].is_completed_by(profile))

        
    def test_complete_1_1(self):
        # bob has one child in the fixture user tree
        profile = self.get_profile('bob')
        self.assert_completion(profile, '1_1')

    
    def test_complete_1_2(self):
        # franck has completed Boost 1/2
        profile = self.get_profile('franck')
        self.assert_completion(profile, '1_2')

    
    def test_complete_1_3(self):
        # franck has completed Boost 2/2
        profile = self.get_profile('franck')
        self.assert_completion(profile, '1_3')

    
    def test_complete_2_1(self):
        pass


    def test_complete_2_2(self):
        pass


    def test_complete_2_3(self):
        pass


    def test_complete_2_4(self):
        pass

    def test_complete_2_4(self):
        pass