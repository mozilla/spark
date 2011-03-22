from django.conf import settings
from django.contrib.sites.models import Site

import mock
from nose.tools import eq_
from pyquery import PyQuery as pq
from test_utils import RequestFactory

from spark.tests import TestCase
from spark.urlresolvers import clean_next_url


SITE_DOMAIN = 'spark.mozilla.org'


class CleanNextUrlTestCase(TestCase):
    
    def _clean_next_url(self, next):
        request = RequestFactory().post('/login', {'next': next})
        return clean_next_url(request)


    def test_accepts_relative_path(self):
        eq_('/m/about', self._clean_next_url('/m/about'))


    def test_prepends_a_slash(self):
        eq_('/m/about', self._clean_next_url('m/about'))


    @mock.patch.object(Site.objects, 'get_current')
    def test_ignores_protocol_relative_url_to_different_domain(self, get_current):
        get_current.return_value.domain = SITE_DOMAIN
        eq_(None, self._clean_next_url('//www.different.com'))


    @mock.patch.object(Site.objects, 'get_current')
    def test_ignores_absolute_url_to_different_domain(self, get_current):
        get_current.return_value.domain = SITE_DOMAIN
        eq_(None, self._clean_next_url('http://www.different.com'))


    @mock.patch.object(Site.objects, 'get_current')
    def test_accepts_protocol_relative_url_to_same_domain(self, get_current):
        get_current.return_value.domain = SITE_DOMAIN
        eq_('/some/file/somewhere', self._clean_next_url('//spark.mozilla.org/some/file/somewhere'))


    @mock.patch.object(Site.objects, 'get_current')
    def test_accepts_absolute_url_to_same_domain(self, get_current):
        get_current.return_value.domain = SITE_DOMAIN
        eq_('/m/some_path/', self._clean_next_url('http://spark.mozilla.org/m/some_path/'))


    @mock.patch.object(Site.objects, 'get_current')
    def test_rejects_data_scheme(self, get_current):
        get_current.return_value.domain = SITE_DOMAIN
        eq_(None, self._clean_next_url('data:text/html,<html><script>alert(1)</script></html>'))
        