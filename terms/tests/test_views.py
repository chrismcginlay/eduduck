#terms/tests/test_views.py
from django.test import TestCase

class TermsViewTests(TestCase):

    def test_index_page_200_OK(self):
        response = self.client.get('/terms/')
        self.assertEqual(response.status_code, 200)

    def test_index_page_uses_correct_template(self):
        response = self.client.get('/terms/')
        self.assertTemplateUsed(response, 'terms/terms_base.html')
        self.assertTemplateUsed(response, 'terms/terms_index.html')
        self.assertContains(
            response, "<h2 id='id_page_title'>")
        self.assertContains(
            response, 'Terms and Conditions')

    def test_index_page_contains_links_to_terms(self):
        response = self.client.get('/terms/')
        self.assertContains(
            response, "Privacy Policy</a>")
        self.assertContains(
            response, "Browsing EduDuck.com</a>")
        self.assertContains(
            response, "Enrolling on a course</a>")
        self.assertContains(
            response, "Creating Content</a>")
        self.assertContains(
            response, "Website Disclaimer</a>")    

    def test_disclaimer_page_200_OK(self):
        response = self.client.get('/terms/disclaimer/')
        self.assertEqual(response.status_code, 200)

    def test_disclaimer_page_uses_correct_template(self):
        response = self.client.get('/terms/disclaimer/')
        self.assertTemplateUsed(response, 'terms/terms_base.html')
        self.assertTemplateUsed(response, 'terms/terms_disclaimer.html')
        self.assertContains(
            response, "<h2 id='id_page_title'>")
        self.assertContains(
            response, 'Website Disclaimer')

    def test_privacy_page_200_OK(self):
        response = self.client.get('/terms/privacy/')
        self.assertEqual(response.status_code, 200)

    def test_privacy_page_uses_correct_template(self):
        response = self.client.get('/terms/privacy/')
        self.assertTemplateUsed(response, 'terms/terms_base.html')
        self.assertTemplateUsed(response, 'terms/terms_privacy.html')
        self.assertContains(
            response, "<h2 id='id_page_title'>")
        self.assertContains(
            response, 'Privacy and Data Protection')

    def test_browsing_page_200_OK(self): 
        response = self.client.get('/terms/browsing/')
        self.assertEqual(response.status_code, 200)

    def test_browsing_page_uses_correct_template(self):
        response = self.client.get('/terms/browsing/')
        self.assertTemplateUsed(response, 'terms/terms_base.html')
        self.assertTemplateUsed(response, 'terms/terms_browsing.html')
        self.assertContains(
            response, "<h2 id='id_page_title'>")
        self.assertContains(
            response, 'Terms and Conditions for Browsing the Website')

    def test_enrolling_page_200_OK(self):
        response = self.client.get('/terms/enrolling/')
        self.assertEqual(response.status_code, 200)

    def test_enrolling_page_uses_correct_template(self):
        response = self.client.get('/terms/enrolling/')
        self.assertTemplateUsed(response, 'terms/terms_base.html')
        self.assertTemplateUsed(response, 'terms/terms_enrolling.html')
        self.assertContains(
            response, "<h2 id='id_page_title'>")
        self.assertContains(
            response, 'Terms and Conditions for Enrolling on a Course')
    
    def test_creating_page_200_OK(self):
        response = self.client.get('/terms/creating/')
        self.assertEqual(response.status_code, 200)
    
    def test_creating_page_uses_correct_template(self):
        response = self.client.get('/terms/creating/')
        self.assertTemplateUsed(response, 'terms/terms_base.html')
        self.assertTemplateUsed(response, 'terms/terms_creating.html')
        self.assertContains(
            response, "<h2 id='id_page_title'>")
        self.assertContains(
            response, 'Terms and Conditions for Creating Content')
