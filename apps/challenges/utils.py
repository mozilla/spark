# -*- coding: utf-8 -*-

from tower import ugettext_lazy as _lazy, ungettext


challenges = {
    # Level 1
    '1_1': _lazy(u'Share your Spark with one other person'),
    '1_2': _lazy(u'Add your location'),
    '1_3': _lazy(u'Tell us where you got your Spark'),
    
    # Level 2
    '2_1': _lazy(u'Obtain a share from Facebook'),
    '2_2': _lazy(u'Obtain a share from Twitter'),
    '2_3': _lazy(u'Sign in on both your phone and your desktop Web browser'),
    '2_4': _lazy(u'Complete a face-to-face share via the QR code on your phone'),
    # L10n: Keep the value of 100 even if 'miles' must be localized to kilometers.
    '2_5': _lazy(u'Share with someone new who lives over 100 miles away'),
    '2_6': _lazy(u'Share with someone new in a different country'),
    '2_7': _lazy(u'Complete 13 shares'),

    # Level 3
    '3_1': _lazy(u'Share with someone between 6am and 10am (Local time for the recipient.)'),
    '3_2': _lazy(u'Share with someone via a printed flyer'),
    '3_3': _lazy(u'Share with someone new on a different continent'),
    '3_4': _lazy(u'Complete 3 shares in a single 12-hour period'),
    '3_5': _lazy(u"Create a chain by having someone you've shared with share with someone else"),
    '3_6': _lazy(u'Complete 20 shares'),

    # Level 4
    '4_1': _lazy(u'Share with someone between 2am and 4am (Local time for the recipient.)'),
    '4_2': _lazy(u'Share your Spark to 8 different U.S. states'),
    '4_3': _lazy(u'Share your Spark to 5 different E.U. countries'),
    '4_4': _lazy(u'Complete 6 shares within a single 12-hour period'),
    '4_5': _lazy(u'Complete 2 or more shares in a single hour'),
    '4_6': _lazy(u'Complete 40 shares'),

    # Super Sparker
    '5_1': _lazy(u'Share with 60 people'),
    '5_2': _lazy(u'Share with 100 people'),
    '5_3': _lazy(u'Share with 250 people'),
    '5_4': _lazy(u'Share with 500 people'),
    '5_5': _lazy(u'Share with 1000 people'),

    # Easter eggs
    'E_1': _lazy(u'Non-Android user who shares with three people'),
    'E_2': _lazy(u'Non-Android user who shares with ten people'),
    'E_3': _lazy(u'Share your Spark to 3 continents'),
    'E_4': _lazy(u'Share your Spark to all 7 continents'),
    'E_5': _lazy(u'Share to Antarctica'),
    'E_6': _lazy(u'Share to Arctic Circle'),
    'E_7': _lazy(u'Share to the capital of any country'),
    'E_8': _lazy(u'Share between the US and UK'),
    'E_9': _lazy(u'Share with someone in each of the 10 different timezones'),
    'E_10': _lazy(u'Share your Spark with someone on an island (Hawaii, Japan, etc.)'),
    'E_11': _lazy(u'Share your Spark to someone in a French-speaking country'),
    'E_12': _lazy(u'Share with someone roughly on the other side of the globe'),
    'E_13': _lazy(u'Share your Spark between a North and South American city'),
    'E_14': _lazy(u'Share to a country with a desert in it'),
    'E_15': _lazy(u'Share to a friend in each of the original 13 US states'),
    'E_16': _lazy(u'Share to someone in each continental state'),
    'E_17': _lazy(u'Share with someone in each original EU country'),
    'E_18': _lazy(u'Share to or from Brazil'),
    'E_19': _lazy(u'Person with the most shares'),
}

badges = {
    # L10n: Badge title for challenge: "Share your Spark with one other person"
    '1_1': [_lazy(u'The Ember'),
    # L10n: Description for "The Ember" badge
            _lazy(u'Congrats on your first share!')],
    # L10n: Badge title for challenge: "Add your location"
    '1_2': [_lazy(u'On Location'),
    # L10n: Description for "On Location" badge
            _lazy(u'You added your location. Nice one!')],
    # L10n: Badge title for challenge: "Tell us where you got your Spark"
    '1_3': [_lazy(u'Parent Trap'),
    # L10n: Description for "Parent Trap" badge
            _lazy(u'You told us where you got your Spark from. Kudos to you!')],

    # L10n: Badge title for challenge: "Obtain a share from Facebook"
    '2_1': [_lazy(u'Socialized'),
    # L10n: Description for "Socialized" badge
            _lazy(u'Did someone get a spark from Facebook? High five!')],
    # L10n: Badge title for challenge: "Obtain a share from Twitter"
    '2_2': [_lazy(u'Twitter Treat'),
    # L10n: Description for "Twitter Treat" badge
            _lazy(u"You got a spark from Twitter. Now that's something to tweet about!")],
    # L10n: Badge title for challenge: "Sign in on both your phone and your desktop Web browser"
    '2_3': [_lazy(u'Multi-sparker'),
    # L10n: Description for "Multi-sparker" badge
            _lazy(u'Looks like someone double-dipped and signed in via their phone and desktop. Score!')],
    # L10n: Badge title for challenge: "Complete a face-to-face share via the QR code on your phone"
    '2_4': [_lazy(u'Face Off'),
    # L10n: Description for "Face Off" badge
            _lazy(u'You did a little face-to-face sharing using your QR code to score.')],
    # L10n: Badge title for challenge: "Share with someone new who lives over 100 miles away"
    '2_5': [_lazy(u'Miles Away'),
    # L10n: Description for "Miles Away" badge
            _lazy(u'You shared with someone new who lives over 100 miles away! You must be exhausted.')],
    # L10n: Badge title for challenge: "Share with someone new in a different country"
    '2_6': [_lazy(u'Long Distance Relationship'),
    # L10n: Description for "Long Distance Relationship" badge
            _lazy(u'Congrats! You shared with someone new in a different country!')],
    # L10n: Badge title for challenge: "Complete 13 shares"
    '2_7': [_lazy(u"Baker's Dozen"),
    # L10n: Description for "Baker's Dozen" badge
            _lazy(u'You shared your Spark 13 times! Welcome to the club!')],

    # L10n: Badge title for challenge: "Share with someone between 6am and 10am (Local time for the recipient.)"
    '3_1': [_lazy(u'Dawn Patrol'),
    # L10n: Description for "Dawn Patrol" badge
            _lazy(u'Anyone up and sharing sparks between 6am and 10am surely deserves this badge.')],
    # L10n: Badge title for challenge: "Share with someone via a printed flyer"
    '3_2': [_lazy(u'Street Team'),
    # L10n: Description for "Street Team" badge
            _lazy(u'Nice! You shared your Spark via a flyer.')],
    # L10n: Badge title for challenge: "Share with someone new on a different continent"
    '3_3': [_lazy(u'Continental Crown'),
    # L10n: Description for "Continental Crown" badge
            _lazy(u'We bow down to you for sharing with someone on another continent.')],
    # L10n: Badge title for challenge: "Complete 3 shares in a single 12-hour period"
    '3_4': [_lazy(u'Triple Threat'),
    # L10n: Description for "Triple Threat" badge
            _lazy(u'3 shares in 12 hours? Well done!')],
    # L10n: Badge title for challenge: "Create a chain by having someone you've shared with share with someone else"
    '3_5': [_lazy(u'Chain Gang'),
    # L10n: Description for "Chain Gang" badge
            _lazy(u'You started a sharing chain. You champ!')],
    # L10n: Badge title for challenge: "Complete 20 shares"
    '3_6': [_lazy(u'XX Sparks'),
    # L10n: Description for "XX Sparks" badge
            _lazy(u'Sharing your Spark 20 times deserves a badge!')],


    # L10n: Badge title for challenge: "Share with someone between 2am and 4am. (Local time for the recipient.)"
    '4_1': [_lazy(u'Night Shift'),
    # L10n: Description for "Night Shift" badge
            _lazy(u'Sharing sparks between 2 and 4 am? Way to go!')],
    # L10n: Badge title for challenge: "Share your Spark to 8 different U.S. states"
    '4_2': [_lazy(u'Octo-sparker'),
    # L10n: Description for "Octo-sparker" badge
            _lazy(u'You shared your Spark to 8 different U.S. states. Good work!')],
    # L10n: Badge title for challenge: "Share your Spark to 5 different E.U. countries"
    '4_3': [_lazy(u'Euroflame'),
    # L10n: Description for "Euroflame" badge
            _lazy(u"You're so cultured! Sharing to 5 different E.U. countries? Amazing!")],
    # L10n: Badge title for challenge: "Complete 6 shares within a single 12-hour period"
    '4_4': [_lazy(u'Optimal Velocity'),
    # L10n: Description for "Optimal Velocity" badge
            _lazy(u'6 shares in 12 hours? You rockstar!')],
    # L10n: Badge title for challenge: "Complete 2 or more shares in a single hour"
    '4_5': [_lazy(u'Speed Spark'),
    # L10n: Description for "Speed Spark" badge
            _lazy(u'You shared 2 or more times in 1 single hour! Well done!')],
    # L10n: Badge title for challenge: "Complete 40 shares"
    '4_6': [_lazy(u'XL Sparks'),
    # L10n: Description for "XL Sparks" badge
            _lazy(u"You've shared 40 sparks! Awesome!")],

    # L10n: Badge title for challenge: "Share with 60 people"
    '5_1': [_lazy(u'Super 60'),
    # L10n: Description for "Super 60" badge
            _lazy(u'60 shares and counting! YEAH!')],
    # L10n: Badge title for challenge: "Share with 100 people"
    '5_2': [_lazy(u'Hundred Hitter'),
    # L10n: Description for "Hundred Hitter" badge
            _lazy(u'100 shares? Happy century!')],
    # L10n: Badge title for challenge: "Share with 250 people"
    '5_3': [_lazy(u'Super 250'),
    # L10n: Description for "Super 250" badge
            _lazy(u'Welcome to superhero status. 250 shares!')],
    # L10n: Badge title for challenge: "Share with 500 people"
    '5_4': [_lazy(u'Super 500'),
    # L10n: Description for "Super 500" badge
            _lazy(u'WOW! You shared with 500 people? Speechless!')],
    # L10n: Badge title for challenge: "Share with 1000 people"
    '5_5': [_lazy(u'Super 1000'),
    # L10n: Description for "Super 1000" badge
            _lazy(u"1000 shares? Can someone say, 'Hall of Fame?'")],

    # L10n: Badge title for challenge: "Non-Android user who shares with three people"
    'E_1': [_lazy(u'Trifecta'),
    # L10n: Description for "Trifecta" badge
            _lazy(u'You shared the Spark with 3 people! Nice one!')],
    # L10n: Badge title for challenge: "Non-Android user who shares with ten people"
    'E_2': [_lazy(u"You're a Dime"),
    # L10n: Description for "You're a Dime" badge
            _lazy(u'10 shares? Way to root for us!')],
    # L10n: Badge title for challenge: "Share your Spark to 3 continents"
    'E_3': [_lazy(u'Backpacker'),
    # L10n: Description for "Backpacker" badge
            _lazy(u'Congrats on sharing your Spark to 3 different continents!')],
    # L10n: Badge title for challenge: "Share your Spark to all 7 continents"
    'E_4': [_lazy(u'Super 7'),
    # L10n: Description for "Super 7" badge
            _lazy(u'You sparked all 7 continents! Way to go!')],
    # L10n: Badge title for challenge: "Share to Antarctica"
    'E_5': [_lazy(u'Penguin Suit'),
    # L10n: Description for "Penguin Suit" badge
            _lazy(u'Look at you, sharing your Spark all the way to Antarctica!')],
    # L10n: Badge title for challenge: "Share to Arctic Circle"
    'E_6': [_lazy(u'Polar Power'),
    # L10n: Description for "Polar Power" badge
            _lazy(u"Brrr. I bet it's cold in the Arctic Circle. Good thing you shared your Spark there.")],
    # L10n: Badge title for challenge: "Share to the capital of any country"
    'E_7': [_lazy(u'Capital Power'),
    # L10n: Description for "Capital Power" badge
            _lazy(u"Here's to you, capital sparker!")],
    # L10n: Badge title for challenge: "Share between the US and UK"
    'E_8': [_lazy(u'Puddle Jumper'),
    # L10n: Description for "Puddle Jumper" badge
            _lazy(u'Sharing the Spark between the US and UK? Snaps to you trans-atlantic sparker!')],
    # L10n: Badge title for challenge: "Share with someone in each of the 10 different timezones"
    'E_9': [_lazy(u'Time Warp'),
    # L10n: Description for "Time Warp" badge
            _lazy(u'10 different timezones? Where did you find all the time?')],
    # L10n: Badge title for challenge: "Share your Spark with someone on an island (Hawaii, Japan, etc)".
    'E_10': [_lazy(u'Island Hopper'),
    # L10n: Description for "Island Hopper" badge
             _lazy(u'You shared to an island. Cool, man!')],
    # L10n: Badge title for challenge: "Share your Spark to someone in a French-speaking country"
    'E_11': [_lazy(u'Vive la Lumi&egrave;re'),
    # L10n: Description for "Vive la Lumière" badge
             _lazy(u'Ohh la la! Someone shared their Spark to a French-speaking country. Tr&egrave;s bon!')],
    # L10n: Badge title for challenge: "Share with someone roughly on the other side of the globe"
    'E_12': [_lazy(u'Earth Sandwich'),
    # L10n: Description for "Earth Sandwich" badge
             _lazy(u'You shared your Spark halfway round the world! Earth Sandwich!')],
    # L10n: Badge title for challenge: "Share your Spark between a North and South American city"
    'E_13': [_lazy(u'Pan Americano'),
    # L10n: Description for "Pan Americano" badge
             _lazy(u'Your Spark crossed the border between North & South America! Ariba!')],
    # L10n: Badge title for challenge: "Share to a country with a desert in it"
    'E_14': [_lazy(u'Feel the Heat'),
    # L10n: Description for "Feel the Heat" badge
             _lazy(u'You shared your Spark to a country with a desert! Well done!')],
    # L10n: Badge title for challenge: "Share to a friend in each of the original 13 US states"
    'E_15': [_lazy(u'The Colonial'),
    # L10n: Description for "The Colonial" badge
             _lazy(u'Looks like someone shared to all original 13 states. What a record!')],
    # L10n: Badge title for challenge: "Share to someone in each continental state"
    'E_16': [_lazy(u'All American'),
    # L10n: Description for "All American" badge
             _lazy(u'Wow! You shared to each continental state? You trooper!')],
    # L10n: Badge title for challenge: "Share with someone in each original EU country"
    'E_17': [_lazy(u'Brussels'),
    # L10n: Description for "Brussels" badge
             _lazy(u'Talk about well-connected. You shared to each original EU country.')],
    # L10n: Badge title for challenge: "Share to or from Brazil"
    'E_18': [_lazy(u'The Amazon'),
    # L10n: Description for "The Amazon" badge
             _lazy(u'Ola! Looks like someone did a little sharing to or from Brazil. Nice!')],
    # L10n: Badge title for challenge: "Person with the most shares"
    'E_19': [_lazy(u'Spark Hall of Famer'),
    # L10n: Description for "Spark Hall of Famer" badge
             _lazy(u'Most shares earns you this much coveted badge. Welcome to the Spark Hall of Fame. Congratulations!')],
}


# L10n: Short description of any challenge level. Example: "Level 3"
LEVEL_GENERIC = _lazy(u'Level %(num)d')

# L10n: Name of the 'Super Sparker' secret level.
LEVEL_5 = _lazy(u'The Super Sparker')



def get_level_description(level):
    desc = ''
    if level == 5:
        desc = unicode(LEVEL_5)
    elif level >= 1 and level < 5:
        desc = unicode(LEVEL_GENERIC) % dict(num=level)
    
    return desc


def get_locked_legend(count, level):
    # L10n: Legend associated to a locked challenge. Example: "You must complete at least 1 challenge in Level 1 to unlock this level."
    msg = ungettext('You must complete at least %(count)d challenge in Level %(level)d to unlock this level.',
                    'You must complete at least %(count)d challenges in Level %(level)d to unlock this level.', count)

    return msg % {'count': count, 'level': level}


def get_challenge_id(level, number):
    if level == 6:
        return 'E_%d' % number
    else:
        return '%d_%d' % (level, number)

