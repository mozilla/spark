# Django settings file for a project based on the playdoh template.

import os
import datetime

from django.utils.functional import lazy

# Make file paths relative to settings.
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

ROOT_PACKAGE = os.path.basename(ROOT)


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

DATABASES = {}  # See settings_local.

# Site ID is used by Django's Sites framework.
SITE_ID = 1


## Internationalization.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Gettext text domain
TEXT_DOMAIN = 'messages'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'


KNOWN_LANGUAGES_STAGE = ('en-US', 'ca', 'de', 'el', 'es', 'eu', 'fr', 'fy', 'hu',
                         'it', 'ko', 'nl', 'pl', 'si', 'sl', 'sq', 'th', 'vi',
                         'zh-TW')
KNOWN_LANGUAGES_PROD = ('en-US','ca','fr','de','it','ja','pl','es','vi',)

# Accepted locales
KNOWN_LANGUAGES = KNOWN_LANGUAGES_PROD


# List of RTL locales known to this project. Subset of LANGUAGES.
RTL_LANGUAGES = ()  # ('ar', 'fa', 'fa-IR', 'he')

LANGUAGE_URL_MAP = dict([(i.lower(), i) for i in KNOWN_LANGUAGES])

# Override Django's built-in with our native names
class LazyLangs(dict):
    def __new__(self):
        from product_details import product_details
        return dict([(lang.lower(), product_details.languages[lang]['native'])
                     for lang in KNOWN_LANGUAGES])

# Where to store product details etc.
PROD_DETAILS_DIR = path('lib/product_details_json')

LANGUAGES = lazy(LazyLangs, dict)()

# paths that don't require a locale prefix
SUPPORTED_NONLOCALES = ('media', 'robots.txt')

## Media and templates.

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = path('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1iz#v0m55@h26^m6hxk3a7at*h$qj_2a$juu1#nv50548j(x1v'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',

    'spark.context_processors.i18n',
    #'jingo_minify.helpers.build_ids',
)

TEMPLATE_DIRS = (
    path('templates'),
)

def JINJA_CONFIG():
    import jinja2
    from django.conf import settings
#    from caching.base import cache
    config = {'extensions': ['tower.template.i18n', 'jinja2.ext.do',
                             'jinja2.ext.with_', 'jinja2.ext.loopcontrols'],
              'finalize': lambda x: x if x is not None else ''}
#    if 'memcached' in cache.scheme and not settings.DEBUG:
        # We're passing the _cache object directly to jinja because
        # Django can't store binary directly; it enforces unicode on it.
        # Details: http://jinja.pocoo.org/2/documentation/api#bytecode-cache
        # and in the errors you get when you try it the other way.
#        bc = jinja2.MemcachedBytecodeCache(cache._cache,
#                                           "%sj2:" % settings.CACHE_PREFIX)
#        config['cache_size'] = -1 # Never clear the cache
#        config['bytecode_cache'] = bc
    return config

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
MINIFY_BUNDLES = {
    'css': {
        'desktop': (
            'css/screen.css',
        ),
        'mobile': (
            'css/mobile.css',
        ),
        'visualization': (
            'css/visualization.css',
        ),
        'non-firefox': (
            'css/non-firefox.css',
        ),
        'badges': (
            'css/badges.css',
        )
    },
    'js': {
        'common': (
            'js/libs/jquery-1.4.4.min.js',
        ),
        'jquery-ui': (
            'js/libs/jquery-ui-1.8.9.custom.min.js',
        ),
        'modernizr': (
            'js/libs/modernizr-1.6.min.js',
        ),
        'raphael': (
            'js/libs/raphael.min.js',
        ),
        'pngfix': (
            'js/libs/DD_belatedPNG_0.0.8a.min.js',
        ),
        'desktop': (
            'js/libs/jquery.form.js',
            'js/libs/placeholder.js',
            'js/desktop/main.js',
            'js/desktop/popupforms.js',
        ),
        'home': (
            'js/desktop/popups-loggedout.js',
            'js/libs/customforms.js',
            'js/libs/jquery.cookie.js'
        ),
        'dashboard': (
            'js/desktop/minimap.js',
            'js/desktop/dashboard.js',
            'js/desktop/sharehistory.js',
            'js/desktop/popups-youraccount.js',
            'js/desktop/popups-boost.js',
            'js/libs/customforms.js',
            'js/desktop/myspark.js',
        ),
        'user-logged-in': (
            'js/desktop/minimap.js',
            'js/desktop/dashboard.js',
            'js/desktop/sharehistory.js',
            'js/desktop/myspark.js',
        ),
        'user-logged-out': (
            'js/desktop/minimap.js',
            'js/desktop/dashboard.js',
            'js/desktop/sharehistory.js',
            'js/desktop/popups-loggedout.js',
            'js/desktop/myspark.js',
        ),
        'pwreset': (
            'js/desktop/popup-pwreset.js',
        ),
        'visualization': (
            'js/desktop/popups-loggedout.js',
            'js/desktop/visualization/raphael-zpd.js',
            'js/desktop/visualization/raphael-group.js',
            'js/desktop/visualization/state.js',
            'js/desktop/visualization/ui.js',
            'js/desktop/visualization/ui-timer.js',
            'js/desktop/visualization/animation.js',
            'js/desktop/visualization/init-raphael.js',
        ),
        'menu': (
            'js/mobile/menu.js',
        ),
        'badges': (
            'js/mobile/badges.js',
        ),
        'geolocation': (
            'js/libs/geolocation.js',
        ),
        'customforms': (
            'js/libs/customforms.js',
        ),
        'myspark': (
            'js/mobile/myspark.js',
        )
    }
}


## Middlewares, apps, URL configs.

MIDDLEWARE_CLASSES = (
    'spark.middleware.LocaleURLMiddleware',
    'spark.middleware.Forbidden403Middleware',
    'spark.middleware.RemoveSlashMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    'mobility.middleware.XMobileMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'commonware.middleware.FrameOptionsHeader',
)

ROOT_URLCONF = '%s.urls' % ROOT_PACKAGE

INSTALLED_APPS = (
    # Third-party apps
    'commonware.response.cookies',
    'djcelery',
    'django_nose',

    # Django contrib apps
    'django.contrib.auth',
    'django_sha2',  # Load after auth to monkey-patch it.
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    # 'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # L10n
    'product_details',

    # Local apps
    'jingo_minify',
    'tower',  # for ./manage.py extract (L10n)

    # We need this so the jsi18n view will pick up our locale directory.
    ROOT_PACKAGE,

    # Newsletter
    'responsys',

    # Spark apps
    'spark',
    'users',
    'desktop',
    'mobile',
    'sharing',
    'challenges',
    'stats',
    'sharing',
    'poster'
)

# Let Tower know about our additional keywords.
# DO NOT import an ngettext variant as _lazy.
TOWER_KEYWORDS = {
    '_lazy': None,
}

TOWER_ADD_HEADERS = True

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS = {
    'geo': [
        ('lib/geo/**.py',
            'tower.management.commands.extract.extract_tower_python'),
    ],
    'messages': [
        ('vendor/**', 'ignore'),
        ('apps/**.py',
            'tower.management.commands.extract.extract_tower_python'),
        ('**/templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
    ],

    ## Use this if you have localizable HTML files:
    #'lhtml': [
    #    ('**/templates/**.lhtml',
    #        'tower.management.commands.extract.extract_tower_template'),
    #],

    ## Use this if you have localizable JS files:
    #'javascript': [
    #    # We can't say **.js because that would dive into any libraries.
    #    ('media/js/desktop/*.js', 'javascript'),
    #    ('media/js/mobile/*.js', 'javascript'),
    #],
}

STANDALONE_DOMAINS = ['messages', 'geo']

# Path to Java. Used for compress_assets.
JAVA_BIN = '/usr/bin/java'

## Auth
AUTHENTICATION_BACKENDS = ('django_sha2.auth.Sha512Backend',)

## Tests
TEST_RUNNER = 'test_utils.runner.RadicalTestSuiteRunner'

## Celery
BROKER_HOST = 'localhost'
BROKER_PORT = 5672
BROKER_USER = 'spark'
BROKER_PASSWORD = 'spark'
BROKER_VHOST = 'spark'
BROKER_CONNECTION_TIMEOUT = 0.1
CELERY_RESULT_BACKEND = 'amqp'
CELERY_IGNORE_RESULT = True
CELERY_ENABLED = True

# Addresses email comes from
DEFAULT_FROM_EMAIL = 'test@localhost.spark'

# Profile Model retrieved via user.get_profile()
AUTH_PROFILE_MODULE = 'users.Profile'

# Responsys: dev/stage key
RESPONSYS_ID = 'X0Gzc2X%3DUQpglLjHJlTQTtQ1vQ2rQ0bQQzgQvQy8KVwjpnpgHlpgneHmgJoXX0Gzc2X%3DUQpglLjHJlTQTtQ1vQ2rQ0aQQGQvQwPD'
MOZILLA_CAMPAIGN = 'MOZILLA_AND_YOU'
SPARK_CAMPAIGN = 'SPARK_2011'
RESPONSYS_URL = 'http://awesomeness.mozilla.org/pub/rf'

# Mobile detection (django-mobility middleware)
MOBILE_COOKIE = 'mobile'

# Session cookies must not be sent over HTTP
SESSION_COOKIE_SECURE = True

# Campaign starting date used by the visualization -- to be changed in settings_local.py
CAMPAIGN_STARTING_DATE = datetime.datetime(2011, 3, 26, 17)

# Facebook App ID
FB_APP_ID = 195624900473285
