import threading
import urlparse

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import reverse as django_reverse
from django.utils.translation.trans_real import parse_accept_lang_header
from django.contrib.sites.models import Site

# Thread-local storage for URL prefixes. Access with (get|set)_url_prefix.
_locals = threading.local()


def set_url_prefixer(prefixer):
    """Set the Prefixer for the current thread."""
    _locals.prefixer = prefixer


def get_url_prefixer():
    """Get the Prefixer for the current thread, or None."""
    return getattr(_locals, 'prefixer', None)


def reverse(viewname, urlconf=None, args=None, kwargs=None, prefix=None,
            force_locale=False, locale=None):
    """Wraps Django's reverse to prepend the correct locale.

    force_locale -- Ordinarily, if get_url_prefixer() returns None, we return
        an unlocalized URL, which will be localized via redirect when visited.
        Set force_locale to True to force the insertion of a default locale
        when there is no set prefixer. If you are writing a test and simply
        wish to avoid LocaleURLMiddleware's initial 301 when passing in an
        unprefixed URL, it is probably easier to substitute LocalizingClient
        for any uses of django.test.client.Client and forgo this kwarg.

    locale -- By default, reverse prepends the current locale (if set) or
        the default locale if force_locale == True. To override this behavior
        and have it prepend a different locale, pass in the locale parameter
        with the desired locale. When passing a locale, the force_locale is
        not used and is implicitly True.

    """
    if locale:
        prefixer = Prefixer(locale=locale)
    else:
        prefixer = get_url_prefixer()
        if not prefixer and force_locale:
            prefixer = Prefixer()

    if prefixer:
        prefix = prefix or '/'
    url = django_reverse(viewname, urlconf, args, kwargs, prefix)
    if prefixer:
        return prefixer.fix(url)
    else:
        return url


def find_supported(test):
    return [settings.LANGUAGE_URL_MAP[x] for
            x in settings.LANGUAGE_URL_MAP if
            x.split('-', 1)[0] == test.lower().split('-', 1)[0]]


def split_path(path):
    """
    Split the requested path into (locale, path).

    locale will be empty if it isn't found.
    """
    path = path.lstrip('/')

    # Use partition instead of split since it always returns 3 parts
    first, _, rest = path.partition('/')

    lang = first.lower()
    if lang in settings.LANGUAGE_URL_MAP:
        return settings.LANGUAGE_URL_MAP[lang], rest
    else:
        supported = find_supported(first)
        if supported:
            return supported[0], rest
        else:
            return '', path


class Prefixer(object):
    def __init__(self, request=None, locale=None):
        """If request is omitted, fall back to a default locale."""
        self.request = request or WSGIRequest({'REQUEST_METHOD': 'bogus'})
        self.locale, self.shortened_path = split_path(self.request.path_info)
        if locale:
            self.locale = locale

    def get_language(self):
        """
        Return a locale code we support on the site using the
        user's Accept-Language header to determine which is best. This
        mostly follows the RFCs but read bug 439568 for details.
        """
        if 'lang' in self.request.GET:
            lang = self.request.GET['lang'].lower()
            if lang in settings.LANGUAGE_URL_MAP:
                return settings.LANGUAGE_URL_MAP[lang]

        if self.request.META.get('HTTP_ACCEPT_LANGUAGE'):
            best = self.get_best_language(
                self.request.META['HTTP_ACCEPT_LANGUAGE'])
            if best:
                return best
        return settings.LANGUAGE_CODE

    def get_best_language(self, accept_lang):
        """Given an Accept-Language header, return the best-matching language."""
        LUM = settings.LANGUAGE_URL_MAP
        PREFIXES = dict((x.split('-')[0], LUM[x]) for x in LUM)
        langs = dict(LUM)
        langs.update((k.split('-')[0], v) for k, v in LUM.items() if
                      k.split('-')[0] not in langs)
        ranked = parse_accept_lang_header(accept_lang)
        for lang, _ in ranked:
            lang = lang.lower()
            if lang in langs:
                return langs[lang]
            pre = lang.split('-')[0]
            if pre in langs:
                return langs[pre]
        # Could not find an acceptable language.
        return False

    def fix(self, path):
        path = path.lstrip('/')
        url_parts = [self.request.META['SCRIPT_NAME']]
        
        first = path.partition('/')[0]
        if first not in settings.SUPPORTED_NONLOCALES:
            locale = self.locale if self.locale else self.get_language()
            if locale == 'ja' and first == 'm':
                locale = 'en-US'
            url_parts.append(locale)

        url_parts.append(path)

        return '/'.join(url_parts)


def clean_next_url(request):
    if 'next' in request.POST:
        url = request.POST.get('next')
    elif 'next' in request.GET:
        url = request.GET.get('next')
    else:
        url = None

    if url:
        parsed_url = urlparse.urlparse(url)
        site_domain = Site.objects.get_current().domain
        next_domain = parsed_url.netloc
        
        if url.startswith('data:'):
            return None
        
        if next_domain:
            if site_domain != next_domain:
                # Don't let absolute or protocol relative URLs redirect outside of Spark.
                return None
            else:
                # Don't include protocol+domain, so if we are https we stay that way.
                url = u'?'.join([getattr(parsed_url, x) for x in
                                ('path', 'query') if getattr(parsed_url, x)])

        # Prepend a '/' to the url if not present. We only want relative URLs.
        if not url.startswith('/'):
            url = '/' + url

        # Don't redirect right back to login or logout page
        auth_urls = [reverse('users.mobile_login'), reverse('users.login'), 
                     reverse('users.logout'), reverse('users.mobile_logout')]
        if parsed_url.path in auth_urls:
            url = None

    return url


def absolute_reverse(view_name):
    return absolute_url(reverse(view_name))


def absolute_url(url):
    site = Site.objects.get_current()
    return u'https://%s%s' % (site, url)


