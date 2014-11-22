#profile/tests/test_utils.py
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase
from social.backends.google import GoogleOAuth2#,FacebookOAuth2

from ..utils import get_image_path, get_user_avatar

class TestProfileUtilities(TestCase):

    fixtures = [
        'auth_user.json', 
    ]
 
    def test_get_user_avatar_for_facebook(self):
        f = get_user_avatar
        self.fail("figure out, or abandon?")

    def test_get_user_avatar_for_google_oauth2(self):
        backend = GoogleOAuth2
        user = get_object_or_404(User, id=1)
        get_user_avatar(backend, user, response, *args, **kwargs)

    def test_get_image_path(self):
        person = User.objects.get(pk=1)
        p = get_image_path(person, 'test.jpg')
        self.assertEqual(p, "/avatars/{0}/test.jpg".format(person.id))

 
