# profile/utilitiesi
from os import remove
from os.path import exists,join
from urllib2 import urlopen
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.utils.text import slugify
from social.backends.facebook import FacebookOAuth2
from social.backends.google import GoogleOAuth2

def get_user_avatar(backend, user, response, *args, **kwargs):
    if isinstance(backend, GoogleOAuth2):
        if response.get('image') and response['image'].get('url'):
            url = response['image'].get('url')

            path = get_image_path(user.profile)
            fullpath = join(settings.MEDIA_ROOT, path)
            if exists(fullpath):
                remove(fullpath)
            user.profile.avatar.save(
                path,
                ContentFile(urlopen(url).read()),
            )
    
    if isinstance(backend, FacebookOAuth2):
        if response.get('id'):
            url = response('id').get('url')
            
#    if isinstance(backend, Twitter):
#        if response.get('profile_image_url'):
#            url = response.get('profile_image_url', '').replace('_normal','')


def get_image_path(profile, filename=None):
    """Construct and return a filepath for user avatar images."""

    user = profile.user
    name_construct = u"{0}_id_{1}".format(user.username, user.id)
    slug_username = slugify(name_construct)
    path = "avatars/{0}/{1}".format(user.id, slug_username+'.jpg')
    return path


