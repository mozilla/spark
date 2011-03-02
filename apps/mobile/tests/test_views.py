from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

import mock
from nose.tools import eq_
from pyquery import PyQuery as pq

from spark.tests import TestCase, LocalizingClient
from spark.urlresolvers import reverse


class BoostStep1TestCase(TestCase):
    fixtures = ['boost.json']
    
    def setUp(self):
        self.client = LocalizingClient()
        self.url = reverse('mobile.boost1')
        self.fake_geo_data = {'lat': 48.8,
                              'long': 2.3,
                              'city': 'Paris',
                              'country': 'France',
                              'country_code': 'FR'}
    
    def test_must_be_logged_in_user(self):
        response = self.client.post(self.url, self.fake_geo_data)
        eq_(302, response.status_code)
        
    def test_user_has_already_completed_boost1(self):
        self.client.login(username='franck', password='testpass')
        response = self.client.post(self.url, self.fake_geo_data)
        eq_(302, response.status_code)
    
    def test_valid_geolocation_info(self):
        self.client.login(username='bob', password='testpass')
        response = self.client.post(self.url, self.fake_geo_data)
        eq_(200, response.status_code)
        doc = pq(response.content)
        eq_(1, len(doc('#your-location')))

    def test_incomplete_geolocation_data(self):
        self.client.login(username='bob', password='testpass')
        data = self.fake_geo_data
        data.update({'city': '', 'country_code': ''})
        response = self.client.post(self.url, data)
        eq_(200, response.status_code)
        doc = pq(response.content)
        eq_(1, len(doc('ul.errorlist li')))

    def test_invalid_geolocation_data(self):
        self.client.login(username='bob', password='testpass')
        data = self.fake_geo_data
        data.update({'country_code': "BAD"})
        response = self.client.post(self.url, data)
        eq_(200, response.status_code)
        doc = pq(response.content)
        eq_(1, len(doc('ul.errorlist li')))

