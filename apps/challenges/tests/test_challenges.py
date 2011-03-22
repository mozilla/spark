import logging
from datetime import datetime, timedelta

from spark.tests import TestCase
from nose.tools import eq_

from geo.continents import (AFRICA, ASIA, EUROPE, NORTH_AMERICA, SOUTH_AMERICA,
                            OCEANIA, ANTARCTICA)

from users.models import User
from stats.models import SharingHistory

from challenges.challenges import all_challenges



class ChallengesTestCase(TestCase):
    fixtures = ['boost.json', 'challenges.json']

    def get_profile(self, username):
        return User.objects.get(username=username).profile


    def assert_completion(self, profile, challenge_id):
        eq_(True, all_challenges[challenge_id].is_completed_by(profile))
    
    def assert_non_completion(self, profile, challenge_id):
        eq_(False, all_challenges[challenge_id].is_completed_by(profile))

        
    def test_complete_1_1(self):
        profile = self.get_profile('bob')
        eq_(0, profile.total_shares)
        SharingHistory.add_share(profile)
        
        profile = self.get_profile('bob')
        eq_(1, profile.total_shares)
        
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
        profile = self.get_profile('bob')
        eq_(0, profile.total_shares)
        SharingHistory.add_share_from_facebook(profile)
        self.assert_completion(profile, '2_1')


    def test_complete_2_2(self):
        profile = self.get_profile('bob')
        eq_(0, profile.total_shares)
        SharingHistory.add_share_from_twitter(profile)
        self.assert_completion(profile, '2_2')


    def test_complete_2_3(self):
        profile = self.get_profile('bob')
        eq_(False, profile.login_desktop)
        profile.login_desktop = True
        self.assert_completion(profile, '2_3')


    def test_complete_2_4(self):
        profile = self.get_profile('bob')
        eq_(0, profile.total_shares)
        SharingHistory.add_share_from_qr_code(profile)
        self.assert_completion(profile, '2_4')


    def test_complete_2_5(self):
        profile = self.get_profile('batman')
        child = profile.children_profiles[0]

        self.assert_non_completion(profile, '2_5')
        
        # Paris
        profile.boost1_completed = True
        profile.latitude = 48.857487002645485
        profile.longitude = 2.3291015625
        profile.save()
        
        # Close to Paris (< 100km)
        child.boost1_completed = True
        child.latitude = 48.821332549646634
        child.longitude = 2.4993896484375
        child.save()
        
        self.assert_non_completion(profile, '2_5')
        
        # Barcelona
        child.boost1_completed = True
        child.latitude = 41.387917
        child.longitude = 2.169918
        child.save()
        
        self.assert_completion(profile, '2_5')


    def test_complete_2_6(self):
        profile = self.get_profile('batman')
        eq_(None, profile.country_code)
        
        profile.country_code = 'US'
        profile.save()
        self.assert_non_completion(profile, '2_6')
        
        child = profile.children_profiles[0]
        child.boost1_completed = True
        child.country_code = 'US'
        child.save()
        self.assert_non_completion(profile, '2_6')
        
        child.country_code = 'MX'
        child.save()
        self.assert_completion(profile, '2_6')


    def test_complete_2_7(self):
        profile = self.get_profile('bob')
        eq_(0, profile.total_shares)
        
        for i in range(13):
            SharingHistory.add_share(profile)
        
        eq_(13, profile.total_shares)
        self.assert_completion(profile, '2_7')


    def test_complete_3_2(self):
        profile = self.get_profile('bob')
        eq_(0, profile.total_shares)
        SharingHistory.add_share_from_poster(profile)
        self.assert_completion(profile, '3_2')
        

    def test_complete_3_3(self):
        profile = self.get_profile('batman')
        profile.boost1_completed = True
        profile.country_code = 'US'
        eq_(NORTH_AMERICA, profile.continent_code)
        
        child = profile.children_profiles[0]
        child.boost1_completed = True
        child.country_code = 'CA'
        child.save()
        eq_(NORTH_AMERICA, child.continent_code)
        self.assert_non_completion(profile, '3_3')
        
        child.country_code = 'FR'
        child.save()
        eq_(EUROPE, child.continent_code)
        self.assert_completion(profile, '3_3')
    
    
    def test_complete_3_4(self):
        profile = self.get_profile('bob')
        eq_(0, profile.total_shares)
        
        now = datetime.now()
        _create_share(profile, now - timedelta(hours=15))
        _create_share(profile, now - timedelta(hours=8))
        _create_share(profile, now - timedelta(hours=3))
        eq_(3, profile.total_shares)
        self.assert_non_completion(profile, '3_4')
        
        _create_share(profile, now - timedelta(hours=11))
        eq_(4, profile.total_shares)
        self.assert_completion(profile, '3_4')
    
    
    def test_complete_3_5(self):
        pass
        
        
    
        
        
        
def _create_share(profile, date):
    share = SharingHistory.objects.create(parent=profile)
    share.date_shared = date
    share.save()








