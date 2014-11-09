from django.core.exceptions import ValidationError
from django.test import TestCase

from django.contrib.auth.models import User

from ..models import Profile 
from ..forms import ProfileEditForm      

class ProfileFormTests(TestCase):
    """Test the operation of profile forms"""
    
    profile1_data = {'user_tz':         "Europe/Paris",
                 'accepted_terms':  True,
                 'signature_line':  'Some catchy signature.',
                 'description':     'Detailed multiline description.',
                 'webpage':         'http://www.unpossible.info',
                 }

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()  
        
        #populate profile + save
        for key,val in self.profile1_data.items():
            self.user1.profile.__dict__[key] = val
        self.user1.profile.save()
        
    def test_profileeditform(self):
        f = ProfileEditForm(instance = self.user1.profile)
        self.assertTrue(isinstance(f.instance, Profile))
        self.assertEqual(f.instance.pk, self.user1.pk)
