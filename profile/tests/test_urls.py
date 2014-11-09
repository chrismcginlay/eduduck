# Test the profile urls (previously known as bio)
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

class UrlTests(TestCase):
    def test_profile(self):
        url = reverse('profile')
        self.assertEqual(url, '/accounts/profile/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'profile')
 
    def test_profile_edit(self):
        url = reverse('profile_edit')
        self.assertEqual(url, '/accounts/profile/edit/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'profile_edit')

    def test_profile_public(self):
        url = reverse('profile_public', kwargs={'user_id':'1'})
        self.assertEqual(url, '/accounts/profile/1/public/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'profile_public')
        self.assertEqual(resolver.kwargs, {'user_id':'1'})

