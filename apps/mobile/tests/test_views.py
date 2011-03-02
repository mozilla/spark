from django.conf import settings
from django.http import HttpResponseRedirect

from nose.tools import eq_
from pyquery import PyQuery as pq

from spark.tests import TestCase, LocalizingClient
from spark.urlresolvers import reverse

from mobile import forms
from users.models import User


class BoostTestCase(TestCase):
    fixtures = ['boost.json']

    def test_user_has_already_completed_both_steps(self):
        client = LocalizingClient()
        client.login(username='franck', password='testpass')
        response = client.get(reverse('mobile.boost'))
        eq_(302, response.status_code)


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

class BoostStep2TestCase(TestCase):
    fixtures = ['boost.json']
    
    def setUp(self):
        self.client = LocalizingClient()
        self.url = reverse('mobile.boost2')
    
    def _assert_result_contains(self, message, response):
        doc = pq(response.content)
        eq_(1, len(doc('#boost2-result')))
        print doc('#boost2-result').text()
        assert message in doc('#boost2-result').text()
    
    def _assert_error_eq(self, error_message, response):
        doc = pq(response.content)
        error = doc('ul.errorlist li')
        eq_(1, len(error))
        eq_(error_message, error.text())
    
    def test_user_has_already_completed_boost2(self):
        self.client.login(username='franck', password='testpass')
        response = self.client.post(self.url, {'identifier': 'bob'})
        eq_(302, response.status_code)
    
    def test_find_by_email_address(self):
        self.client.login(username='bob', password='testpass')
        response = self.client.post(self.url, {'identifier': 'franck'})
        eq_(200, response.status_code)
        self.assertContains(response, 'boost2-result')
        self._assert_result_contains('Your Spark was started by', response)

    def test_find_by_username(self):
        self.client.login(username='bob', password='testpass')
        response = self.client.post(self.url, {'identifier': 'franck@test.com'})
        eq_(200, response.status_code)
        self.assertContains(response, 'boost2-result')
        self._assert_result_contains('Your Spark was started by', response)
    
    def test_started_a_spark_on_my_own(self):
        self.client.login(username='bob', password='testpass')
        response = self.client.post(self.url, {'from_website': True})
        eq_(200, response.status_code)
        self.assertContains(response, 'boost2-result')
        self._assert_result_contains('Congrats! You started a new Spark', response)
    
    def test_share_with_yourself(self):
        self.client.login(username='bob', password='testpass')
        response = self.client.post(self.url, {'identifier': 'bob'})
        eq_(200, response.status_code)
        self._assert_error_eq(unicode(forms.IDENTIFIER_SELF), response)        
    
    def test_identifier_notfound(self):
        self.client.login(username='bob', password='testpass')
        response = self.client.post(self.url, {'identifier': 'unknown_username'})
        eq_(200, response.status_code)
        self._assert_error_eq(unicode(forms.IDENTIFIER_NOTFOUND), response)


class BoostStep2ConfirmationTestCase(TestCase):
    fixtures = ['boost.json']

    def setUp(self):
        self.client = LocalizingClient()
        self.url = reverse('mobile.boost2_confirm')

    def test_invalid_request(self):
        self.client.login(username='bob', password='testpass')
        response = self.client.post(self.url, {'wrong_data': 'test'})
        eq_(400, response.status_code)

    def test_invalid_parent(self):
        self.client.login(username='bob', password='testpass')
        response = self.client.post(self.url, {'parent': 'franck'})
        eq_(400, response.status_code)
        
    def test_relationship_created(self):
        self.client.login(username='bob', password='testpass')
        response = self.client.post(self.url, {'parent': 'john'})
        assert isinstance(response, HttpResponseRedirect)
        eq_('http://testserver/en-US%s' % reverse('mobile.home'), response['location'])
        
        bob = User.objects.get(username='bob')
        john = User.objects.get(username='john')
        eq_(bob.node.parent, john.node)
        eq_(True, bob.get_profile().boost2_completed)

    def test_no_parent_confirm(self):
        self.client.login(username='john', password='testpass')
        response = self.client.post(self.url, {'no_parent': True})
        assert isinstance(response, HttpResponseRedirect)
        eq_('http://testserver/en-US%s' % reverse('mobile.home'), response['location'])
        
        profile = User.objects.get(username='john').get_profile()
        eq_(True, profile.boost2_completed)

