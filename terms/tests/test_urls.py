#terms/tests/test_urls.py
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

class TermsUrlTests(TestCase):
    def test_TermsIndex(self):
        url = reverse('terms:terms_index')
        self.assertEqual(url, '/terms/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'terms:terms_index')

    def test_TermsPrivacyPolicy(self):
        url = reverse('terms:terms_privacy')
        self.assertEqual(url, '/terms/privacy/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'terms:terms_privacy')

    def test_TermsBrowsingWebsite(self):
        url = reverse('terms:terms_browsing')
        self.assertEqual(url, '/terms/browsing/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'terms:terms_browsing')

    def test_TermsEnrollingOnCourse(self):
        url = reverse('terms:terms_enrolling')
        self.assertEqual(url, '/terms/enrolling/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'terms:terms_enrolling')

    def test_TermsCreatingContent(self):
        url = reverse('terms:terms_creating')
        self.assertEqual(url, '/terms/creating/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'terms:terms_creating')

    def test_TermsWebsiteDisclaimer(self):
        url = reverse('terms:terms_disclaimer')
        self.assertEqual(url, '/terms/disclaimer/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'terms:terms_creating')
