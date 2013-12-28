from django.core.urlresolvers import reverse
from django.db import models
from django.http import Http404
from django.contrib.auth.models import User
from bio.models import Bio


class Course(models.Model):
    """A self contained course of study.
    
    Attributes:
        code         Course code for human consumption
        name         Human readable name of course
        abstract     Summary paragraph outlining course
        organiser    Foreign key: user organising course
        instructor   Foreign key: user providing instruction 
        level        Level of difficulty of this course (eg SCQF)
        credits      Number of points awarded on completion
       
    """

    code = models.CharField(max_length=10, 
                                   help_text="arbitrary course code for "
                                   "author's reference")
    name = models.CharField(max_length=150, 
                                   help_text="human readable name of "
                                   "the course")
    abstract = models.TextField(help_text="summary of the course "
                                "in a couple of paragraphs")
                                           
    organiser = models.ForeignKey(User,
                                  related_name="courses_organised_set",
                                  help_text="This user is organising the course")
    instructor = models.ForeignKey(User,
                                   related_name="courses_instructed_set",
                                   help_text="This user is providing the instruction")
    level = models.CharField(max_length=10, blank=True, null=True,
                             help_text="e.g. SCQF level")
    credits = models.IntegerField(blank=True, null=True,)

    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""

        super (Course, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            assert self.code
            assert self.name
            assert self.organiser
            assert self.instructor
            #NB level is a string (eg. 'Foundation', '2')
            assert self.level
            assert self.credits >= 0
        
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        assert self.id >=1
        return reverse(u"courses.views.single", kwargs= {'course_id': self.id})
        
        
class Lesson(models.Model):
    """A digestible chunk of learning material within a course.
    
    Attributes:
        code     	Lesson code for human consumption
        name     	Human readable full lesson name
        course          ForeignKey - course to which lesson belongs
        abstract        short text description of the lesson
        
    """
    
    code = models.CharField(max_length=10, blank=True, null=True,
                            help_text="arbitrary lesson code for "
                            "author's reference")
    name = models.CharField(max_length=200)
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
            assert self.code
            assert self.name
            assert self.course
        
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        assert self.course
        assert self.id
        return reverse(u"courses.views.lesson", kwargs = { 
                'course_id': self.course.id,
                'lesson_id': self.id })
        
        
class Video(models.Model):
    """Details of video resources used in lessons.
    
    Note that videos may have foreign keys directly to a course, not just 
    to lessons. This allows for introductory videos to belong to whole course
        
    Attributes:
        code  Video code for human consumption
        name  Full human readable name of video
        url         url of the video resource
        lesson      ForeignKey - if the video is embedded in a lesson
        course      ForeignKey - if the video is embedded directly in course    
    """
    
    #TODO: use YouTube / Vimeo APIs to pull video meta data such as title, tags    
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=200)
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
            assert self.code
            assert self.url
            assert self.name

    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return self.url
        
