from django.template import Template, Context, TemplateSyntaxError

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
        self.user1 = User.objects.create_user("bertie", u"bert@bert.com", 'bertword')
        self.user1.is_active = True
        self.user1.save()    
        
    def test_gravatar_url(self):
        """Gravatar url produced correctly"""

        e, sz = self.user1.email, u'40'
        gun = GravatarUrlNode(e, sz)
        #gpn = GravatarProfileNode(e, sz)

        self.assertEqual(e, gun.email.var, 'Tag fails to parse email address')
        self.assertEqual(sz, gun.size.var, 'Tag fails to parse size')

        out = Template(
            	"{% load gravatar %}" \
                "{% gravatar_url 'bert@bert.com' 30 %}")
        context = Context({"user": self.user1,
                           "size": 30})
        
        #import pdb; pdb.set_trace();
        
        target = u"http://www.gravatar.com/avatar/3caa837c41ae74577aad7e307be4d028?s=30&d=wavatar"
        self.assertEqual(out.render(context), target, "Gravatar tag failed")
