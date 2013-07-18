from django.db import models
from django.http import Http404
from django.contrib.auth.models import User
from bio.models import Bio

import pdb

class Course(models.Model):
    """A self contained course of study.
    
    Attributes:
        course_code         Course code for human consumption
        course_name         Human readable name of course
        course_abstract     Summary paragraph outlining course
        course_organiser    Person responsible for this course
        course_level        Level of difficulty of this course (eg SCQF)
        course_credits      Number of points awarded on completion
       
    """

    course_code = models.CharField(max_length=10, 
                                   help_text="arbitrary course code for "
                                   "author's reference")
    course_name = models.CharField(max_length=150, 
                                   help_text="human readable name of "
                                   "the course")
    course_abstract = models.TextField(help_text="summary of the course "
                                       "in a couple of paragraphs")
                                           
    #TODO change this to ForeignKey(User)
    course_organiser = models.CharField(max_length=100)
    course_level = models.CharField(max_length=10, blank=True, null=True,
                                    help_text="e.g. SCQF level")
    course_credits = models.IntegerField(blank=True, null=True,)

    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (Course, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            assert self.course_code
            assert self.course_name
            assert self.course_organiser
            #NB course_level is a string (eg. 'Foundation', '2')
            assert self.course_level
            assert self.course_credits >= 0
        
    def __unicode__(self):
        return self.course_name
    
    @models.permalink
    def get_absolute_url(self):
        assert self.id >=1
        return ('courses.views.single', [str(self.id)])
        
        
class Lesson(models.Model):
    """A digestible chunk of learning material within a course.
    
    Attributes:
        lesson_code     Lesson code for human consumption
        lesson_name     Human readable full lesson name
        course          ForeignKey - course to which lesson belongs
        abstract        short text description of the lesson
        
    """
    
    lesson_code = models.CharField(max_length=10, blank=True, null=True,
                                   help_text="arbitrary lesson code for "
                                   "author's reference")
    lesson_name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, 
                               help_text="course to which this "
                               "lesson belongs")
    abstract = models.TextField(help_text="summary of the lesson "
                                       "in a couple of paragraphs")

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
            assert self.lesson_code
            assert self.lesson_name
            assert self.course
        
    def __unicode__(self):
        return self.lesson_name
    
    @models.permalink
    def get_absolute_url(self):
        assert self.course
        assert self.id
        return ('courses.views.lesson', (), {
                'course_id': self.course.id,
                'lesson_id': self.id })
        
        
class Video(models.Model):
    """Details of video resources used in lessons.
    
    Note that videos may have foreign keys directly to a course, not just 
    to lessons. This allows for introductory videos to belong to whole course
        
    Attributes:
        video_code  Video code for human consumption
        video_name  Full human readable name of video
        url         url of the video resource
        lesson      ForeignKey - if the video is embedded in a lesson
        course      ForeignKey - if the video is embedded directly in course
    
    """
    
    #TODO: use YouTube / Vimeo APIs to pull video meta data such as title, tags    
    video_code = models.CharField(max_length=10, blank=True, null=True)
    video_name = models.CharField(max_length=200)
    url = models.URLField()
    #TODO override __init__ to ensure precisely one of these is not null
    lesson = models.ForeignKey(Lesson, blank=True, null=True)
    course = models.ForeignKey(Course, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (Video, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            assert self.video_code
            assert self.url
            assert self.video_name

    def __unicode__(self):
        return self.video_name
    
    def get_absolute_url(self):
        return self.url
        
