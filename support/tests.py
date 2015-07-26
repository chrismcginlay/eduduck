""" Unit tests for Support 'pseudo'-app """

from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

from .forms import SupportForm


class SupportFormTests(TestCase):
    """Test the form used to present a support/contact request"""
     
    def setUp(self):
        """Set up two bound (first valid, second not) and one unbound form"""
        self.f1 = SupportForm({
            'subject':'Hello. Just unit testing support again', 
            'email':'noreply@eduduck.com', 
            'message':'Support is working if you get this. Be happy.'
        })

        self.f2 = SupportForm({
            'subject':None, 
            'email':'noreplyFAILeduduck.com', 
            'message':'Not long enough'
        })
        
        self.f3 = SupportForm()
                             
    def test_support_form_validation(self):
        """Correctly bound/unbound and valid/invalid forms created"""
        
        self.assertEqual(self.f1.is_valid(), True)
        self.assertEqual(self.f2.is_valid(), False)
        self.assertEqual(self.f3.is_valid(), False)
        self.assertEqual(self.f1.is_bound, True)
        self.assertEqual(self.f2.is_bound, True)
        self.assertEqual(self.f3.is_bound, False)
        self.assertEqual(self.f2['message'].errors[0], 
            u"Please muster four or more words of wisdom or woe!")
            
class SupportFormViewTests(TestCase):
    """Test the suppoort form view"""

    def setUp(self):
        pass

    def test_support(self):
        """Test the presence of the support page"""
        response = self.client.get('/support/')
        self.assertEqual(response.status_code, 200)
        
    def test_ssl_logo_area_present(self):
        response = self.client.get('/support/')
        needle = 'id="id_ssl_logo"'
        self.assertIn(needle, response.content)        

    def test_support_thanks(self):
        """Test the presence of the thanks page"""
        response = self.client.get('/support/thanks/')
        self.assertEqual(response.status_code, 200)

class SupportUrlTests(TestCase):
    
    def test_support_url(self):
        url = reverse('support')
        self.assertEqual(url, '/support/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'support')
        
