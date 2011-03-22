import logging
from datetime import datetime, timedelta

from .models import Challenge
from .utils import get_challenge_id as _id

from users.models import UserNode, Profile
from users.utils import user_node

from geo.continents import (AFRICA, ASIA, EUROPE, NORTH_AMERICA, SOUTH_AMERICA,
                            OCEANIA, ANTARCTICA)
from geo.groups import (european_countries, island_countries, countries_with_desert,
                        original_eu_countries, original_us_states, continental_us_states, all_us_states)

from stats.models import SharingHistory, VIA_TWITTER, VIA_FACEBOOK, VIA_QR, VIA_POSTER


all_challenges = {}


class ChallengeImpl:
    """ Base class for the implementation of challenges. """
    def is_completed_by(self, profile):
        return False


class TheEmber(ChallengeImpl):
    """ Share your Spark with one other person """
    def is_completed_by(self, profile):
        return profile.total_shares >= 1

all_challenges[_id(1, 1)] = TheEmber()


class OnLocation(ChallengeImpl):
    """ Add your location """
    def is_completed_by(self, profile):
        return profile.boost1_completed

all_challenges[_id(1, 2)] = OnLocation()


class ParentTrap(ChallengeImpl):
    """ Tell us where you got your Spark """
    def is_completed_by(self, profile):
        return profile.boost2_completed

all_challenges[_id(1, 3)] = ParentTrap()


class Socialized(ChallengeImpl):
    """ Obtain a share from Facebook """
    def is_completed_by(self, profile):
        return SharingHistory.has_gained_shares_via(profile, VIA_FACEBOOK)

all_challenges[_id(2, 1)] = Socialized()


class TwitterThreat(ChallengeImpl):
    """ Obtain a share from Twitter """
    def is_completed_by(self, profile):
        return SharingHistory.has_gained_shares_via(profile, VIA_TWITTER)

all_challenges[_id(2, 2)] = TwitterThreat()


class Multisparker(ChallengeImpl):
    """ Sign in on both your phone and your desktop Web browser """
    def is_completed_by(self, profile):
        return profile.login_desktop

all_challenges[_id(2, 3)] = Multisparker()


class FaceOff(ChallengeImpl):
    """ Complete a face-to-face share via the QR code on your phone """
    def is_completed_by(self, profile):
        return SharingHistory.has_gained_shares_via(profile, VIA_QR)

all_challenges[_id(2, 4)] = FaceOff()


class MilesAway(ChallengeImpl):
    """ Share with someone new who lives over 100 miles away """
    def is_completed_by(self, profile):
        from spark.utils import distance
        
        DISTANCE = 160.9344 # 100 miles to km
        
        if profile.boost1_completed:
            for child in profile.children_profiles:
                if (child.boost1_completed and distance((profile.latitude, profile.longitude),
                                                        (child.latitude, child.longitude)) >= DISTANCE):
                    return True
        return False

all_challenges[_id(2, 5)] = MilesAway()


class LongDistanceRelationship(ChallengeImpl):
    """ Share with someone new in a different country """
    def is_completed_by(self, profile):
        if profile.boost1_completed:
            for child in profile.children_profiles:
                if child.boost1_completed and (profile.country_code != child.country_code):
                    return True
        return False

all_challenges[_id(2, 6)] = LongDistanceRelationship()


class BakersDozen(ChallengeImpl):
    """ Complete 13 shares """
    def is_completed_by(self, profile):
        return profile.total_shares >= 13

all_challenges[_id(2, 7)] = BakersDozen()

class DawnPatrol(ChallengeImpl):
    """ Share with someone between 6am and 10am (Local time for the recipient.) """
    def is_completed_by(self, profile):
        return False

all_challenges[_id(3, 1)] = DawnPatrol()

class StreetTeam(ChallengeImpl):
    """ Share with someone via a printed flyer """
    def is_completed_by(self, profile):
        return SharingHistory.has_gained_shares_via(profile, VIA_POSTER)

all_challenges[_id(3, 2)] = StreetTeam()

class ContinentalCrown(ChallengeImpl):
    """ Share with someone new on a different continent """
    def is_completed_by(self, profile):
        if profile.boost1_completed:
            for child in profile.children_profiles:
                if child.boost1_completed and (profile.continent_code != child.continent_code):
                    return True
        return False

all_challenges[_id(3, 3)] = ContinentalCrown()

class TripleThreat(ChallengeImpl):
    """ Complete 3 shares in a single 12-hour period """
    def is_completed_by(self, profile):
        if profile.total_shares >= 3:
            now = datetime.now()
            share = SharingHistory.objects.order_by('-date_shared')[2]
            if share and (share.date_shared > now - timedelta(hours=12)):
                return True
        return False

all_challenges[_id(3, 4)] = TripleThreat()

class ChainGang(ChallengeImpl):
    """ Create a chain by having someone you've shared with share with someone else """
    def is_completed_by(self, profile):
        return profile.longest_chain >= 2

all_challenges[_id(3, 5)] = ChainGang()

class XXSparks(ChallengeImpl):
    """ Complete 20 shares """
    def is_completed_by(self, profile):
        return profile.total_shares >= 20

all_challenges[_id(3, 6)] = XXSparks()

class NightShift(ChallengeImpl):
    """ Share with someone between 2am and 4am. (Local time for the recipient.) """
    def is_completed_by(self, profile):
        return False

all_challenges[_id(4, 1)] = NightShift()

class OctoSparker(ChallengeImpl):
    """ Share your Spark to 8 different U.S. states """
    def is_completed_by(self, profile):
        children_states = set([child.us_state for child in profile.children_profiles])
        return len(children_states) >= 8

all_challenges[_id(4, 2)] = OctoSparker()

class Euroflame(ChallengeImpl):
    """ Share your Spark to 5 different E.U. countries """
    def is_completed_by(self, profile):
        countries = set()
        for child in profile.children_profiles:
            if child.country_code and country_continents[child.country_code] == EUROPE:
                countries.add(child.country_code)
        return len(countries) >= 5

all_challenges[_id(4, 3)] = Euroflame()

class OptimalVelocity(ChallengeImpl):
    """ Complete 6 shares within a single 12-hour period """
    def is_completed_by(self, profile):
        if profile.total_shares >= 6:
            now = datetime.now()
            share = SharingHistory.objects.order_by('-date_shared')[5]
            if share and (share.date_shared > now - timedelta(hours=12)):
                return True
        return False

all_challenges[_id(4, 4)] = OptimalVelocity()

class SpeedSpark(ChallengeImpl):
    """ Complete 2 or more shares in a single hour """
    def is_completed_by(self, profile):
        if profile.total_shares >= 2:
            now = datetime.now()
            share = SharingHistory.objects.order_by('-date_shared')[1]
            if share and (share.date_shared > now - timedelta(hours=1)):
                return True
        return False

all_challenges[_id(4, 5)] = SpeedSpark()

class XLSparks(ChallengeImpl):
    """ Complete 40 shares """
    def is_completed_by(self, profile):
        return profile.total_shares >= 40

all_challenges[_id(4, 6)] = XLSparks()

class Super60(ChallengeImpl):
    """ Share with 60 people """
    def is_completed_by(self, profile):
        return profile.total_shares >= 60

all_challenges[_id(5, 1)] = Super60()

class HundredHitter(ChallengeImpl):
    """ Share with 100 people """
    def is_completed_by(self, profile):
        return profile.total_shares >= 100

all_challenges[_id(5, 2)] = HundredHitter()

class Super250(ChallengeImpl):
    """ Share with 250 people """
    def is_completed_by(self, profile):
        return profile.total_shares >= 250

all_challenges[_id(5, 3)] = Super250()

class Super500(ChallengeImpl):
    """ Share with 500 people """
    def is_completed_by(self, profile):
        return profile.total_shares >= 500

all_challenges[_id(5, 4)] = Super500()

class Super1000(ChallengeImpl):
    """ Share with 1000 people """
    def is_completed_by(self, profile):
        return profile.total_shares >= 1000

all_challenges[_id(5, 5)] = Super1000()

class Trifecta(ChallengeImpl):
    """ Non-Android user who shares with three people """
    def is_completed_by(self, profile):
        return profile.is_non_android and profile.total_shares >= 3

all_challenges[_id(6, 1)] = Trifecta()

class YoureADime(ChallengeImpl):
    """ Non-Android user who shares with ten people """
    def is_completed_by(self, profile):
        return profile.is_non_android and profile.total_shares >= 10

all_challenges[_id(6, 2)] = YoureADime()

class Backpacker(ChallengeImpl):
    """ Share your Spark to 3 continents """
    def is_completed_by(self, profile):
        return profile.total_continents_sparked >= 3

all_challenges[_id(6, 3)] = Backpacker()

class Super7(ChallengeImpl):
    """ Share your Spark to all 7 continents """
    def is_completed_by(self, profile):
        return profile.total_continents_sparked == 7

all_challenges[_id(6, 4)] = Super7()

class PenguinSuit(ChallengeImpl):
    """ Share to Antarctica """
    def is_completed_by(self, profile):
        for child in profile.children_profiles:
            if child.continent_code and child.continent_code == ANTARCTICA:
                return True
        return False

all_challenges[_id(6, 5)] = PenguinSuit()

class PolarPower(ChallengeImpl):
    """ Share to Arctic Circle """
    def is_completed_by(self, profile):
        for child in profile.children_profiles:
            if child.latitude and child.latitude > 66.5622:
                return True
        return False

all_challenges[_id(6, 6)] = PolarPower()

class CapitalPower(ChallengeImpl):
    """ Share to the capital of any country """
    def is_completed_by(self, profile):
        return False

all_challenges[_id(6, 7)] = CapitalPower()

class PuddleJumper(ChallengeImpl):
    """ Share between the US and UK """
    def is_completed_by(self, profile):
        if profile.country_code == 'UK':
            for child in profile.children_profiles:
                if child.country_code and child.country_code == 'US':
                    return True
        if profile.country_code == 'US':
            for child in profile.children_profiles:
                if child.country_code and child.country_code == 'UK':
                    return True
        return False

all_challenges[_id(6, 8)] = PuddleJumper()

class TimeWarp(ChallengeImpl):
    """ Share with someone in each of the 10 different timezones """
    def is_completed_by(self, profile):
        return False

all_challenges[_id(6, 9)] = TimeWarp()

class IslandHopper(ChallengeImpl):
    """ Share your Spark with someone on an island (Hawaii, Japan, etc) """
    def is_completed_by(self, profile):
        for child in profile.children_profiles:
            if child.country_code and child.country_code in countries_with_island:
                return True
        return False

all_challenges[_id(6, 10)] = IslandHopper()

class ViveLaLumiere(ChallengeImpl):
    """ Share your Spark to someone in a French-speaking country """
    def is_completed_by(self, profile):
        for child in profile.children_profiles:
            if child.country_code and child.country_code in countries_with_island:
                return True
        return False

all_challenges[_id(6, 11)] = ViveLaLumiere()

class EarthSandwich(ChallengeImpl):
    """ Share with someone roughly on the other side of the globe """
    def is_completed_by(self, profile):
        return False

all_challenges[_id(6, 12)] = EarthSandwich()

class PanAmericano(ChallengeImpl):
    """ Share your Spark between a North and South American city """
    def is_completed_by(self, profile):
        if profile.continent_code:
            if profile.continent_code == NORTH_AMERICA:
                for child in profile.children_profiles:
                    if child.continent_code and child.continent_code == SOUTH_AMERICA:
                        return True
            if profile.continent_code == SOUTH_AMERICA:
                for child in profile.children_profiles:
                    if child.continent_code and child.continent_code == NORTH_AMERICA:
                        return True
        return False

all_challenges[_id(6, 13)] = PanAmericano()

class FeelTheHeat(ChallengeImpl):
    """ Share to a country with a desert in it """
    def is_completed_by(self, profile):
        for child in profile.children_profiles:
            if child.country_code and child.country_code in countries_with_desert:
                return True
        return False

all_challenges[_id(6, 14)] = FeelTheHeat()

class TheColonial(ChallengeImpl):
    """ Share to a friend in each of the original 13 US states """
    def is_completed_by(self, profile):
        for child in profile.children_profiles:
            if child.us_state and child.us_state in original_us_states:
                return True
        return False

all_challenges[_id(6, 15)] = TheColonial()

class AllAmerican(ChallengeImpl):
    """ Share to someone in each continental state """
    def is_completed_by(self, profile):
        for child in profile.children_profiles:
            if child.us_state and child.us_state in continental_us_states:
                return True
        return False

all_challenges[_id(6, 16)] = AllAmerican()

class Brussels(ChallengeImpl):
    """ Share with someone in each original EU country """
    def is_completed_by(self, profile):
        for child in profile.children_profiles:
            if child.country_code and child.country_code in original_eu_countries:
                return True
        return False

all_challenges[_id(6, 17)] = Brussels()

class TheAmazon(ChallengeImpl):
    """ Share to or from Brazil """
    def is_completed_by(self, profile):
        if profile.country_code = 'BR':
            return True
        for child in profile.children_profiles:
            if child.country_code and child.country_code == 'BR':
                return True
        return False

all_challenges[_id(6, 18)] = TheAmazon()

class HallOfFamer(ChallengeImpl):
    """ Person with the most shares """
    def is_completed_by(self, profile):
        return False

all_challenges[_id(6, 19)] = HallOfFamer()
