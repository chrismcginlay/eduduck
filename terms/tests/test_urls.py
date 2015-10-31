#terms/tests/test_urls.py
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

class TermsUrlTests(TestCase):
    def test_TermsIndex(self):
        url = reverse('terms:index')
        self.assertEqual(url, '/terms/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'terms:index')

    def test_TermsPrivacyPolicy(self):
        url = reverse('terms:privacy_policy')
        self.assertEqual(url, '/terms/privacy_policy/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'terms:privacy_policy')

    def test_TermsBrowsingWebsite(self):
        url = reverse('terms:browsing')
        self.assertEqual(url, '/terms/browsing/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'terms:browsing')

    def test_TermsEnrollingOnCourse(self):
        url = reverse('terms:enrolling')
        self.assertEqual(url, '/terms/enrolling/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'terms:enrolling')

    def test_TermsCreatingContent(self):
        url = reverse('terms:creating')
        self.assertEqual(url, '/terms/creating/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'terms:creating')


