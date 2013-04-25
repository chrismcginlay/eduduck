from django.core.exceptions import ValidationError
from django.test import TestCase

from django.contrib.auth.models import User

from .models import Bio
from .forms import BioEditForm


class BioModelTests(TestCase):
    """Test the model used to present a user bio"""
     
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
        
    def test_bio_create(self):
        """Automatically create an empty biography
        
        The User postsave hook should mean a bio is created automatically"""
        
        assert(self.user1.bio)
        
    def test_bio_details(self):
        """Check that bio can be populated with canonical data"""
        
        #populate + save
        for key,val in self.bio1_data.items():
            self.user1.bio.__dict__[key] = val
        self.user1.bio.full_clean()
        self.user1.bio.save()
        #check        
        for key,val in self.bio1_data.items():
            self.assertEqual(self.user1.bio.__dict__[key], val)
            
    def test_missing_requiredfield_chokes(self):
        """Check that missing fields are caught"""
        
        #populate
        for key,val in self.bio1_data.items():
            self.user1.bio.__dict__[key] = val
            
        #blank, test, reinstate
        self.user1.bio.signature_line = None
        with self.assertRaises(ValidationError):
            self.user1.bio.full_clean()
        self.user1.bio.signature_line = self.bio1_data['signature_line']

        self.user1.bio.user_tz = None
        with self.assertRaises(ValidationError):
            self.user1.bio.full_clean()
        self.user1.bio.user_tz = self.bio1_data['user_tz']
            

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
        
        #TODO test view redirects valid form.

class BioFormTests(TestCase):
    """Test the operation of bio forms"""
    
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
        
        #populate bio + save
        for key,val in self.bio1_data.items():
            self.user1.bio.__dict__[key] = val
        self.user1.bio.save()
        
    def test_bioeditform(self):
        f = BioEditForm(instance = self.user1.bio)
        self.assertTrue(isinstance(f.instance, Bio))
        self.assertEqual(f.instance.pk, self.user1.pk)
