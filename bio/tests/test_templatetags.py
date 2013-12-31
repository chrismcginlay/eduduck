from django import template

from django.core.exceptions import ValidationError
from django.test import TestCase

from django.contrib.auth.models import User

from ..models import Bio
from ..templatetags.gravatar import GravatarUrlNode

class BioTemplateTagTests(TestCase):
    """Test behaviour of user 'bio' custom template tags"""
    
    bio1_data = {'user_tz':         "Europe/Paris",
                 'accepted_terms':  True,
                 'signature_line':  'Some catchy signature.',
                 'description':     'Detailed multiline description.',
                 'webpage':         'http://www.unpossible.info',
                 }

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bert@bert.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()    
        
    def test_gravatar_url(self):
        """Gravatar url produced correctly"""

        register = template.Library()
        e, sz = self.user1.email, u'40'
        gun = GravatarUrlNode(e, sz)
        #gpn = GravatarProfileNode(e, sz)

        self.assertEqual(e, gun.email.var, 'Tag fails to parse email address')
        self.assertEqual(sz, gun.size.var, 'Tag fails to parse size')

        login = self.client.login(username='bertie', password='bertword')
        self.assertTrue(login)
        response = self.client.get('/accounts/bio/')

        import pdb; pdb.set_trace();
        
        gun_render = gun.render(response.context)
        self.assertEqual(gun_render, u'ddd')
