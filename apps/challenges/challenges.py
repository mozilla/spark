# -*- coding: utf-8 -*-

from tower import ugettext_lazy as _lazy, ungettext


challenges = {
    # Level 1
    'lvl1_ch1': _lazy(u'Share your Spark with one other person'),
    'lvl1_ch2': _lazy(u'Add your location'),
    'lvl1_ch3': _lazy(u'Tell us where you got your Spark'),
    
    # Level 2
    'lvl2_ch1': _lazy(u'Obtain a share from Facebook'),
    'lvl2_ch2': _lazy(u'Obtain a share from Twitter'),
    'lvl2_ch3': _lazy(u'Sign in on both your phone and your desktop Web browser'),
    'lvl2_ch4': _lazy(u'Complete a face-to-face share via the QR code on your phone'),
    # L10n: Keep the value of 100 even if 'miles' must be localized to kilometers.
    'lvl2_ch5': _lazy(u'Share with someone new who lives over 100 miles away'),
    'lvl2_ch6': _lazy(u'Share with someone new in a different country'),
    'lvl2_ch7': _lazy(u'Complete 13 shares'),

    # Level 3
    'lvl3_ch1': _lazy(u'Share with someone between 6am and 10am (Local time for the recipient.)'),
    'lvl3_ch2': _lazy(u'Share with someone via a printed flyer'),
    'lvl3_ch3': _lazy(u'Share with someone new on a different continent'),
    'lvl3_ch4': _lazy(u'Complete 3 shares in a single 12-hour period'),
    'lvl3_ch5': _lazy(u"Create a chain by having someone you've shared with share with someone else"),
    'lvl3_ch6': _lazy(u'Complete 20 shares'),

    # Level 4
    'lvl4_ch1': _lazy(u'Share with someone between 2am and 4am (Local time for the recipient.)'),
    'lvl4_ch2': _lazy(u'Share your Spark to 8 different U.S. states'),
    'lvl4_ch3': _lazy(u'Share your Spark to 5 different E.U. countries'),
    'lvl4_ch4': _lazy(u'Complete 6 shares within a single 12-hour period'),
    'lvl4_ch5': _lazy(u'Complete 2 or more shares in a single hour'),
    'lvl4_ch6': _lazy(u'Complete 40 shares'),

    # Super Sparker
    'lvl5_ch1': _lazy(u'Share with 60 people'),
    'lvl5_ch2': _lazy(u'Share with 100 people'),
    'lvl5_ch3': _lazy(u'Share with 250 people'),
    'lvl5_ch4': _lazy(u'Share with 500 people'),
    'lvl5_ch5': _lazy(u'Share with 1000 people'),

    # Easter eggs
    'ee_ch1': _lazy(u'Non-Android user who shares with three people'),
    'ee_ch2': _lazy(u'Non-Android user who shares with ten people'),
    'ee_ch3': _lazy(u'Share your Spark to 3 continents'),
    'ee_ch4': _lazy(u'Share your Spark to all 7 continents'),
    'ee_ch5': _lazy(u'Share to Antarctica'),
    'ee_ch6': _lazy(u'Share to Arctic Circle'),
    'ee_ch7': _lazy(u'Share to the capital of any country'),
    'ee_ch8': _lazy(u'Share between the US and UK'),
    'ee_ch9': _lazy(u'Share with someone in each of the 10 different timezones'),
    'ee_ch10': _lazy(u'Share your Spark with someone on an island (Hawaii, Japan, etc.)'),
    'ee_ch11': _lazy(u'Share your Spark to someone in a French-speaking country'),
    'ee_ch12': _lazy(u'Share with someone roughly on the other side of the globe'),
    'ee_ch13': _lazy(u'Share your Spark between a North and South American city'),
    'ee_ch14': _lazy(u'Share to a country with a desert in it'),
    'ee_ch15': _lazy(u'Share to a friend in each of the original 13 US states'),
    'ee_ch16': _lazy(u'Share to someone in each continental state'),
    'ee_ch17': _lazy(u'Share with someone in each original EU country'),
    'ee_ch18': _lazy(u'Share to or from Brazil'),
    'ee_ch19': _lazy(u'Person with the most shares'),
}


def get_locked_legend(count, level):
    # L10n: Legend associated to a locked challenge. Example: "You must complete at least 1 challenge in Level 1 to unlock this level."
    msg = ungettext('You must complete at least %(count)d challenge in Level %(level)d to unlock this level.',
                    'You must complete at least %(count)d challenges in Level %(level)d to unlock this level.', count)

    return msg % {'count': count, 'level': level}

def get_locked_legend_alternate(count, level):
    # L10n: Legend associated to a locked challenge. Example: "Complete 4 more challenges in Level 3 to unlock."
    msg = ungettext('Complete %(count)d more challenge in Level %(level)d to unlock.',
                    'Complete %(count)d more challenges in Level %(level)d to unlock.', count)

    return msg % {'count': count, 'level': level}

