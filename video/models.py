from django.db import models
from courses.models import Course, Lesson

# Create your models here.

class Video(models.Model):
    """ URLs and various meta data
    
    Attributes:
        name        Text name of the video for human consumption
        url         Yep.
        lesson      FK to lesson } one of these two must be non-null
        course      FK to course } one of these two must be non-null
        
    """
    
    #TODO: use YouTube / Vimeo APIs to pull video meta data such as title, tags    
    name = models.CharField(max_length=200)
    url = models.URLField()
    #TODO override __init__ to ensure precisely one of these is not null
    lesson = models.ForeignKey(Lesson, blank=True, null=True)
    course = models.ForeignKey(Course, blank=True, null=True)
    
    class Meta:
        unique_together= ("lesson", "course")
    
    #def __init__(self, *args, **kwargs):
        #"""checkrep on instantiation"""
        #super (Video, self).__init__(*args, **kwargs)
        ##When adding a new instance (e.g. in admin), their will be no 
        ##datamembers, so only check existing instances eg. from db load.
        #if self.pk != None:
            #assert self.url
            #assert self.name
            
    def __str__(self):
        return "Video: {0}".format(self.name)

    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return self.url
