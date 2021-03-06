from django.core.urlresolvers import reverse
from django.db import models
from courses.models import Course

import logging
logger = logging.getLogger(__name__)

# Create your models here.

class Lesson(models.Model):
    """A digestible chunk of learning material within a course.
    
    Attributes:
    name        Human readable full lesson name
    course      ForeignKey - course to which lesson belongs
    abstract    short text description of the lesson
    
    """
    
    name = models.CharField(max_length=200, verbose_name='lesson title')
    course = models.ForeignKey(Course, 
                               help_text="course to which this "
                               "lesson belongs")
    abstract = models.TextField(help_text="summary of the lesson "
                                "in a couple of paragraphs")
    
    def _checkrep(self):
        if not self.name:
            logger.warn("Lesson {0} name is empty".format(self.pk))
            return False
        assert self.course
        return True

    def get_next(self):
        """Return the next lesson in the course"""
        assert self.course
        assert self.id
        next = Lesson.objects.filter(course=self.course).filter(id__gt=self.id)
        if next:
            return next[0]
        return False
    
    def get_prev(self):
        """Return the previous lesson in the course"""
        assert self.course
        assert self.id
        prev = Lesson.objects.filter(course=self.course).filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev[0]
        return False
    
    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (Lesson, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            self._checkrep()
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        assert self.course
        assert self.id
        return reverse(u"lesson_visit", kwargs = { 
            'course_id': self.course.id,
            'lesson_id': self.id })
            
