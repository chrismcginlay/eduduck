# profile/utilities
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from social.backends.facebook import FacebookOAuth2
from social.backends.google import GoogleOAuth2

def get_user_avatar(backend, user, response, *args, **kwargs):
    import pdb; pdb.set_trace()
    if isinstance(backend, GoogleOAuth2):
        if response.get('image') and response['image'].get('url'):
            url = response['image'].get('url')

#???
            ext = url.split('.')[-1]
            user.profile.avatar.save(
                '{0}{1}'.format('avatar', ext),
                ImageFile(urllib2.urlopen(url).read()),
                save=False
            )
            user.save()
#???
    if isinstance(backend, FacebookOAuth2):
        if response.get('id'):
            url = response('id').get('url')
            
    if isinstance(backend, Twitter):
        if response.get('profile_image_url'):
            url = response.get('profile_image_url', '').replace('_normal','')

#use ImageFile as above
    if url:
        profile = user.profile()
        avatar = urlopen(url).read()
        fout = open(filepath, "wb")
        fout.write(avatar)
        fout.close()
        profile.avatar = None #path to image
        profile.save

def get_image_path(user, filename):
    """Construct and return a filepath for user avatar images"""

    path = "/avatars/{0}/{1}".format(user.id, filename)
    return path


