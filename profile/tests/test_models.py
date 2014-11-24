from os import remove
from os.path import exists, join
from urllib2 import urlopen
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.test import TestCase

from django.contrib.auth.models import User

from ..models import Profile
from ..forms import ProfileEditForm
from ..utils import get_image_path

class ProfileModelTests(TestCase):
    """Test the model used to present a user profile"""
     
    profile1_data = {
        'user_tz':         "Europe/Paris",
        'accepted_terms':  True,
        'signature_line':  'Some catchy signature.',
        'description':     'Detailed multiline description.',
        'webpage':         'http://www.unpossible.info',
    }

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
    
    def tearDown(self):
        gip = get_image_path(self.user1.profile)
        # Delete avatar from previous tests, if any.
        fullpath = join(settings.MEDIA_ROOT, gip)
        if exists(fullpath):
            remove(fullpath)
 
    def test_profile_create(self):
        """Automatically create an empty profile
        
        The User postsave hook should mean a profile is created automatically"""
        
        assert(self.user1.profile)
       
    def test_profile_with_default_avatar(self):
        """Without social auth, a default profile should be loaded"""
        user2 = User.objects.create_user('florence', 'florence@example.com', 'florence')
        user2.is_active = True
        user2.save()
        target = join(settings.MEDIA_URL, 'avatars/2/florence_id_2.jpg')
        self.assertEqual(user2.profile.avatar.url, target)

    def test_profile_details(self):
        """Check that profile can be populated with canonical data"""
        
        #populate + save
        for key,val in self.profile1_data.items():
            self.user1.profile.__dict__[key] = val
        self.user1.profile.full_clean()
        self.user1.profile.save()
        pk = self.user1.profile.pk
            
    def test_missing_requiredfield_chokes(self):
        """Check that missing fields are caught"""
        
        #populate
        for key,val in self.profile1_data.items():
            self.user1.profile.__dict__[key] = val
            
        #blank, test, reinstate
        self.user1.profile.signature_line = None
        with self.assertRaises(ValidationError):
            self.user1.profile.full_clean()
        self.user1.profile.signature_line = self.profile1_data['signature_line']

        self.user1.profile.user_tz = None
        with self.assertRaises(ValidationError):
            self.user1.profile.full_clean()
        self.user1.profile.user_tz = self.profile1_data['user_tz']
            
    def test___unicode__(self):
        s = self.user1.__unicode__()
        target = self.user1.username
        self.assertEqual(s, target, "Incorrect __unicode__ return")

    def test___str__(self):

        s = self.user1.profile.__str__()
        target = u"Profile: {0} {1}".format(
            self.user1.pk, self.user1.username)
        self.assertEqual(s, target, "Incorrect __str__ return")

    def test_get_absolute_url(self):
        url = self.user1.get_absolute_url()
        target = u"/users/{0}/".format(self.user1.username)
        self.assertEqual(url, target, "Incorrect get_absolute_url return")
        

    def test_get_profile_url(self):
        url = self.user1.profile.get_profile_url()
        target = u"/accounts/profile/{0}/public/".format(self.user1.id)
        self.assertEqual(url, target, "Incorrect get_profile_url return")
