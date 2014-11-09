from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User

import pytz

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

    NB, enrolled courses not recorded here. Instead data relevant to a 
    user's interactions with a course will be recorded in a 'through' 
    model/table.
    """
    
    TIMEZONE_CHOICES = zip(pytz.common_timezones, pytz.common_timezones)
    user = models.OneToOneField(User)
    user_tz = models.CharField(max_length=255, choices=TIMEZONE_CHOICES, 
                                blank=False, null=False)
    accepted_terms = models.BooleanField(null=False, blank=False, default=True)
    signature_line = models.CharField(max_length=200)
    description = models.TextField(max_length=10000,blank = True)
    webpage = models.URLField(blank = True)
    
    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (Profile, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            assert self.user
    
    def __unicode__(self):
        return self.user.username
        
    def __str__(self):
        """For debug mostly"""
        return "Profile: " + str(self.id) + " " + self.user.username

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
