from django.core.exceptions import ValidationError
from django.test import TestCase

from django.contrib.auth.models import User

from ..models import Bio
from ..forms import BioEditForm      

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
