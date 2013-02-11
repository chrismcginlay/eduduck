from django.db import models

from django.contrib.auth.models import User


class Bio(models.Model):
    """Extend user module with additional data"""
    
    """Biographical or 'profile' information about users

    Attributes:
        user                1-1Field - Required field - User
        accepted_terms      Either you do or you don't
        signature_line      Personal motto for user
        description         More detailed description
        webpage             Link to user's webpage.

    NB, registered courses not recorded here. Instead data relevant to a 
    user's interactions with a course will be recorded in a 'through' 
    model/table.
    """
    
    user = models.OneToOneField(User)
    accepted_terms = models.BooleanField(null=False, blank=False)
    signature_line = models.CharField(max_length=200)
    description = models.TextField(max_length=10000,blank = True)
    webpage = models.URLField(blank = True)
    
    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (Bio, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            assert self.user
    
    def __unicode__(self):
        return self.user.username
        
    def __str__(self):
        """For debug mostly"""
        return "Bio:" + str(self.id) + " " + self.user.username
        
    @models.permalink
    def get_absolute_url(self):
        assert self.id
        return ('bio.views.bio', [str(self.id)])