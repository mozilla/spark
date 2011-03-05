import logging

from .models import Challenge
from .utils import get_challenge_id as _id

from users.models import UserNode, Profile
from users.utils import user_node


all_challenges = {}


class ChallengeImpl:
    """ Base class for the implementation of challenges. """
    def is_completed_by(self, user):
        return False


class TheEmber(ChallengeImpl):
    """ Share your Spark with one other person """
    def is_completed_by(self, profile):
        try:
            node = user_node(profile.user)
            return len(node.get_children()) >= 1
        except UserNode.DoesNotExist:
            return False

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
        return False

all_challenges[_id(2, 1)] = Socialized()


class TwitterThreat(ChallengeImpl):
    """ Obtain a share from Twitter """
    def is_completed_by(self, profile):
        return False

all_challenges[_id(2, 2)] = TwitterThreat()


class Multisparker(ChallengeImpl):
    """ Sign in on both your phone and your desktop Web browser """
    def is_completed_by(self, profile):
        return False

all_challenges[_id(2, 3)] = Multisparker()


class FaceOff(ChallengeImpl):
    """ Complete a face-to-face share via the QR code on your phone """
    def is_completed_by(self, profile):
        return False

all_challenges[_id(2, 4)] = FaceOff()


class MilesAway(ChallengeImpl):
    """ Share with someone new who lives over 100 miles away """
    def is_completed_by(self, profile):
        return False

all_challenges[_id(2, 5)] = MilesAway()


class LongDistanceRelationship(ChallengeImpl):
    """ Share with someone new in a different country """
    def is_completed_by(self, profile):
        return False

all_challenges[_id(2, 6)] = LongDistanceRelationship()


class BakersDozen(ChallengeImpl):
    """ Complete 13 shares """
    def is_completed_by(self, profile):
        return False

all_challenges[_id(2, 7)] = BakersDozen()

