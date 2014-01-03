from django.template import Template, Context, TemplateSyntaxError

from django.core.exceptions import ValidationError
from django.test import TestCase

from django.contrib.auth.models import User

from ..models import Bio
from ..templatetags.gravatar import GravatarUrlNode, GravatarProfileNode

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
        
    def text_gravatar_url_node_parsing_two_args(self):
        """Test the tag can parse email and size"""

        e, sz = self.user1.email, u'40'
        gun = GravatarUrlNode(e, sz)

        self.assertEqual(e, gun.email.var, 'Tag fails to parse email address')
        self.assertEqual(sz, gun.size.var, 'Tag fails to parse size')

    def text_gravatar_url_node_parsing_one_args(self):
        """Test the tag can parse email only, supply default size"""

        e = self.user1.email
        gun = GravatarUrlNode(e)

        self.assertEqual(e, gun.email.var, 'Tag fails to parse email address')
        self.assertEqual(30, gun.size.var, 'Tag generates wrong default size')
    
    def test_gravatar_url_email_size(self):
        """Gravatar url produced correctly when both an email and size given"""

        e, sz = self.user1.email, u'40'
        gun = GravatarUrlNode(e, sz)

        out = Template(
            	"{% load gravatar %}" \
                "{% gravatar_url 'bert@bert.com' 40 %}")
        context = Context({"user": self.user1,
                           "size": 40})

        target = u"http://www.gravatar.com/avatar/"\
            "3caa837c41ae74577aad7e307be4d028?s=30&d=wavatar"
        self.assertEqual(out.render(context), target, "Gravatar url tag failed")

    def test_gravatar_url_email_only(self):
        """Gravatar url produced correctly when only an email given"""

        e = self.user1.email
        gun = GravatarUrlNode(e)

        out = Template(
            	"{% load gravatar %}" \
                "{% gravatar_url 'bert@bert.com' %}")
        context = Context({"user": self.user1})
        
        target = u"http://www.gravatar.com/avatar"\
            "/3caa837c41ae74577aad7e307be4d028?s=30&d=wavatar"
        self.assertEqual(out.render(context), target, "Gravatar url tag failed")

    def test_gravatar_url_no_args(self):
        """Gravatar throws exception if no email given"""

        with self.assertRaises(IndexError):
            GravatarUrlNode()

    def test_gravater_profile_node_parsing(self):
        """Check that the argument is correctly parsed"""

        e = self.user1.email
        gpn = GravatarProfileNode(e)

        self.assertEqual(e, gpn.email.var, 'Tag fails to parse email address')

    def test_gravatar_profile(self):
        """Gravatar profile link produced correctly"""

        e = self.user1.email
        gpn = GravatarProfileNode(e)

        out = Template("{% load gravatar %}" \
                       "{% gravatar_profile 'bert@bert.com' %}")
        context = Context({"user": self.user1})
        target = u"http://www.gravatar.com/3caa837c41ae74577aad7e307be4d028"
        self.assertEqual(out.render(context), target, 
                         "Gravatar profile tag failed")

    def test_gravatar_profile_missing_argument(self):
        """Gravatar profile raises exception in absence of email"""

        with self.assertRaises(IndexError):
            gpn = GravatarProfileNode()


