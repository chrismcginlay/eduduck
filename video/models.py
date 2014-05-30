from django.core.exceptions import ValidationError
from django.db import models
from courses.models import Course
from lesson.models import Lesson

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
    lesson = models.ForeignKey(Lesson, blank=True, null=True)
    course = models.ForeignKey(Course, blank=True, null=True)
    
    def __str__(self):
        return "Video: {0}".format(self.name)

    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return self.url
    
    def _checkrep(self):
        if self.name == "": return False
        if self.url == "": return False
        # At least one of these should not be zero:
        if not (self.course or self.lesson): return False
        return True
    
    def __init__(self, *args, **kwargs):
        """Run _checkrep on instantiation"""
        super(Video, self).__init__(*args, **kwargs)
        
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            self._checkrep()
        
    def save(self, *args, **kwargs):
        if (self.lesson == None and self.course == None): raise ValidationError
        if (self.name == '' or self.url == ''): raise ValidationError
        
        super(Video, self).save(*args, **kwargs)
        