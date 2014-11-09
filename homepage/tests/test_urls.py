# Test the homepage urls
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

class UrlTests(TestCase):
    def test_homepage_home(self):
        url = reverse('homepage')
        self.assertEqual(url, '/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'homepage')
 
