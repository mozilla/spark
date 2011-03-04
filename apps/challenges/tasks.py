import logging

from celery.decorators import task

from .models import Challenge
from .challenges import all_challenges


@task
def update_completed_challenges(profile):
    """ Detects if the user has completed new challenges and updates their profile. """
    
    # Retrieve previously completed challenges
    previous_challenges = (unicode(c) for c in profile.challenges.all())
    
    # Loop through all challenges and exclude already completed ones
    non_completed_challenges = ((id, c) for (id, c) in all_challenges.iteritems() if id not in previous_challenges)
    
    # Find newly completed challenges
    completed_challenges = []
    for id, challenge in non_completed_challenges:
        if challenge.is_completed_by(profile):
            completed_challenges.append(id)
    
    # Update the user profile (this awards badges too, since 1 challenge == 1 badge)
    if completed_challenges:
        new_challenges = Challenge.objects.filter(pk__in=completed_challenges)
        for challenge in new_challenges:
            logging.debug("%s was awarded: %s" % (profile.user.username, challenge.get_badge_name()))
            profile.challenges.add(challenge)
        
        # Let's see if the user gained a level
        _update_level(profile)



def _update_level(profile):
    """ Detects if the user has gained one or multiple level(s) and updates their profile. """

    challenges = profile.challenges.all()
    level = profile.level
    
    if level == 1:
        # Complete at least 1 challenge in level 1 to advance
        if len([c for c in challenges if c.level == 1]) >= 1:
            level = 2
    
    if level == 2:
        # Complete at least 4 challenges in level 2 to advance
        if len([c for c in challenges if c.level == 2]) >= 4:
            level = 3
    
    if level == 3:
        # Complete at least 4 challenges in level 3 to advance
        if len([c for c in challenges if c.level == 3]) >= 4:
            level = 4
    
    if level == 4:
        # Complete all challenges below the Super Sparker to advance
        if len([c for c in challenges if c.level < 5]) == 22:
            level = 5
    
    if level != profile.level:
        profile.level = level
        profile.save()

