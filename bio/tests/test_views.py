from django.core.exceptions import ValidationError
from django.test import TestCase

from django.contrib.auth.models import User

from ..models import Bio
from ..forms import BioEditForm


class BioViewTests(TestCase):
    """Test behaviour of user 'bio' views"""
    
    bio1_data = {'user_tz':         "Europe/Paris",
                 'accepted_terms':  True,
                 'signature_line':  'Some catchy signature.',
                 'description':     'Detailed multiline description.',
                 'webpage':         'http://www.unpossible.info',
                 }

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()    
        
    def test_bio(self):
        """Test response bio.views.bio"""
        
        #Not logged in, redirect.
        response = self.client.get('/accounts/bio/')
        #self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/bio/')

        #log in and check bio is available      
        login = self.client.login(username='bertie', password='bertword')
        self.assertTrue(login)
        response = self.client.get('/accounts/bio/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context for x in ['bio', 'usercourses'])
        self.assertIn('Timezone', response.content, "Timezone not rendered")

        #check for existence of password change link
        self.assertIn('<a href="/accounts/password/change/">Change Password</a>', response.content, "Password change link missing")

    def test_bio_edit(self):
        """Test response bio.views.edit"""
        
        #Not logged in, redirect.
        response = self.client.get('/accounts/bio/edit/')
        self.assertRedirects(response, '/accounts/login/?next=/accounts/bio/edit/')  
        
        #log in and check bio is available      
        login = self.client.login(username='bertie', password='bertword')
        self.assertTrue(login)
        response = self.client.get('/accounts/bio/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context for x in ['bio', 'form'])   

        #check for existence of password change link
        self.assertIn('<a href="/accounts/password/change/">Change Password</a>', response.content, "Password change link missing")
        
        #Test form with missing data
        response = self.client.post("/accounts/bio/edit/", kwargs={
                'accepted_terms': "True",
                'signature_line': "Test",
                'description': "Test description",
                'webpage': "www.eduduck.com",
                })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['user_tz'].errors, 
                         [u'This field is required.'])

        #Test form with no data
        response = self.client.post("/accounts/bio/edit/", kwargs={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['user_tz'].errors, 
                         [u'This field is required.'])

        #Test form with complete data
        response = self.client.post("/accounts/bio/edit/", kwargs={
                'user_tz': "US/Pacific",
                'accepted_terms': "True",
                'signature_line': "Test",
                'description': "Test description",
                'webpage': "www.eduduck.com",
                })
        self.assertEqual(response.status_code, 200)

        #Test form with junk data
        response = self.client.post("/accounts/bio/edit/", kwargs={
                'blast': "pants",
                })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['user_tz'].errors, 
                         [u'This field is required.'])

    def test_bio_public(self):
        """Test response bio.public"""
        
        url = "/accounts/bio/public/{0}/".format(self.user1.bio.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context for x in 
                        ['timezone', 'webpage', 'description'])

