from django.core.exceptions import ValidationError
from django.db import models
from courses.models import Course
from lesson.models import Lesson
from video.utils import force_https, validate_youtube_url

from core.eduduck_exceptions import CheckRepError

import logging
logger = logging.getLogger(__name__)

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
    url = models.URLField(validators=[validate_youtube_url])
    lesson = models.ForeignKey(Lesson, blank=True, null=True)
    course = models.ForeignKey(Course, blank=True, null=True)
    
    def __str__(self):
        return "Video: {0}".format(self.name)

    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return self.url
    
    def _checkrep(self):
        if self.name == "":
            logger.warning("Video {0} lacks name".format(self.id))
            return False
        if self.url == "":
            logger.warning("Video {0} lacks url".format(self.id))
            return False
        # Convert any http:// protocols to https://
        if self.url[:7] == "http://":
            self.url = force_https(self.url)
            logger.info("Rewriting https protocol on video {0}".format(self.id))
            self.save()

        # At least one of these should not be zero:
        if not (self.course or self.lesson): 
            logger.error("Orphaned video")
            raise CheckRepError("Video has no FK to course or lesson")
        return True
    
    def __init__(self, *args, **kwargs):
        """Run _checkrep on instantiation"""
        super(Video, self).__init__(*args, **kwargs)
        
        # Convert any http:// protocols to https://
        if self.url[:7] == "http://":
            self.url = force_https(self.url)

        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            self._checkrep()
        
    def save(self, *args, **kwargs):
        if (self.lesson == None and self.course == None):
            logger.error("Orphaned video, save failed")
            raise CheckRepError("Orphaned video: no course or lesson")
        if (self.name == '' or self.url == ''): 
            logger.warning("Video lacks name or url")
            raise ValidationError
        
        super(Video, self).save(*args, **kwargs)
        
