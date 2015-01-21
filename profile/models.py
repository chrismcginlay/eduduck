# profile/models.py
from os.path import join
import pytz

from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models import ImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.text import slugify
from .storage import OverwriteFSStorage
from .utils import get_image_path

import logging
logger = logging.getLogger(__name__)

class Profile(models.Model):
    """Extend user module with additional data"""
    
    """Profile information about users

    Attributes:
        user                1-1Field - Required field - User
        timezone            User's timezone - required.
        accepted_terms      Either you do or you don't
        signature_line      Personal motto for user
        description         More detailed description
        webpage             Link to user's webpage.
        avatar              User avatar image field

    NB, enrolled courses not recorded here. Instead data relevant to a 
    user's interactions with a course will be recorded in a 'through' 
    model/table.
    """
    
    TIMEZONE_CHOICES = zip(pytz.common_timezones, pytz.common_timezones)
    user = models.OneToOneField(User)
    user_tz = models.CharField(max_length=255, choices=TIMEZONE_CHOICES, 
                                blank=False, null=False, default=u"UTC")
    accepted_terms = models.BooleanField(null=False, blank=False, default=True)
    signature_line = models.CharField(max_length=200)
    description = models.TextField(max_length=10000,blank = True)
    webpage = models.URLField(blank = True)
    fs = OverwriteFSStorage(
        base_url=settings.MEDIA_URL, location=settings.MEDIA_ROOT)
    avatar = ImageField(
        upload_to=get_image_path, 
        blank=False, null=False, 
        storage=fs)
 
    def _checkrep(self):
        """Run checkrep on instantiation"""
        if not self.user_tz:
            logger.warning("User {0} has no timezone".format(self.user.pk))
            return False
        if not self.accepted_terms:
            logger.warning(
                "User {0} hasn't accepted terms".format(self.user.pk))
            return False
        assert self.user
        path = join(settings.MEDIA_URL, get_image_path(self.user.profile))
        assert(self.avatar.url==path)
        return True

    def __init__(self, *args, **kwargs):
        super (Profile, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            self._checkrep()
    
    def __unicode__(self):
        return self.user.username
        
    def __str__(self):
        """For debug mostly"""
        return "Profile: " + str(self.id) + " " + self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        if not(self.avatar):
            # Pull in the default avatar
            gip = get_image_path(self)
            # Not using STATIC_ROOT below: 
            # because this is a file open not webserver request
            f = open(join(
                settings.BASE_DIR, 'static/images/default-avatar.jpg'))
            self.avatar.save(
                gip,
                ContentFile(f.read()),
            )

    def get_absolute_url(self):
        assert self.id
        return reverse(u"profile.views.profile")

    def get_profile_url(self):
        """Return url for publicly visible 'profile' or profile"""

        assert self.id
        return reverse(u"profile.views.public", kwargs={'user_id':str(self.id)})

#########################################
#   Signals Area
#########################################

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Ensure user profile is created for each new user"""
    if created:
        Profile.objects.create(user=instance)
