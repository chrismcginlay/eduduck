from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
                                           
    #TODO change this to ForeignKey(UserPrf)
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

# TODO No video view defined yet 
#    @models.permalink
#    def get_absolute_url(self):
#        return ('TODO')
        
#TODO important to validate uploaded files
#see PDF p796.
class Attachment(models.Model):
    """Handle all forms of attachment except video.
    
    Attributes:
        att_code    Attachment code for human consumption
        att_name    Human readable name of the attachment
        lesson      ForeignKey - if attachment embedded in lesson
        course      ForeignKey - if attachment embedded in course
        att_desc    Paragraph describing contents of attachment
        att_seq     Optional unique sequence number of attachment
        attachment  Django file model instance

    """
    
    #TODO: better modules exist for this.
    att_code = models.CharField(max_length=10, blank=True, null=True)
    att_name = models.CharField(max_length=200)
    lesson = models.ForeignKey(Lesson, blank=True, null=True)
    course = models.ForeignKey(Course, blank=True, null=True)
    att_desc = models.TextField(blank=True, null=True)
    att_seq = models.IntegerField(blank=True, null=True)
    attachment = models.FileField(upload_to='attachments')
    
    class Meta:
        unique_together = (("lesson", "att_seq"),)   

    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (Attachment, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            assert self.att_code
            assert self.att_name
            assert self.attachment
            assert (self.lesson or self.course)
        
#       Should anything slip past debug to -O production:
#       Ensure precisely one of the following is not null, reflecting fact
#       that attachment can be linked to lesson or direct to parent course
        if not (self.lesson or self.course):
            raise Http404("Attachment needs to be linked to lesson or course")
        
    def __unicode__(self):
        return self.att_name

# TODO No attachment view defined yet 
#    @models.permalink
#    def get_absolute_url(self):
#        return ('TODO')   


class LearningIntention(models.Model):
    """Link Learning Intentions with individual lessons.
    
    Learning Intention: Specific learning to take place - 
    what you intend to do, e.g. practise using Newton's 2nd Law to predict
    motion of a vehicle.
    
    Attributes:
        lesson      ForiegnKey to parent lesson.
        li_text     Actual text content of the learning intention.
        
    """
    
    lesson = models.ForeignKey(Lesson,
                               help_text="parent lesson for this intention")
    li_text = models.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (LearningIntention, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            assert self.lesson
            assert self.li_text

    def get_next(self):
        """Return the next learning intention in the lesson"""
        assert self.lesson
        assert self.id
        next = LearningIntention.objects.filter(lesson=self.lesson).filter(id__gt=self.id).order_by('id')
        if next:
            return next[0]
        return False
        
    def get_prev(self):
        """Return the previous learning intention in the lesson"""
        assert self.lesson
        assert self.id
        prev = LearningIntention.objects.filter(lesson=self.lesson).filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev[0]
        return False

    def __unicode__(self):
        return self.li_text
        
    def __str__(self):
        """Human readable for debug mostly"""
        return "LI " + str(self.pk) + ": " + self.li_text
        
    @models.permalink
    def get_absolute_url(self):
        assert self.lesson
        assert self.id
        return ('courses.views.learning_intention', (), {
                'lesson_id': self.lesson.id,
                'learning_intention_id': self.id })
              
              
class SuccessCriterion(models.Model):
    """Success criteria link back to individual Learning Intentions
    
    All criteria together for a Learning Intention help to direct the student
    towards achieving a particular (learning) outcome. (A learning outcome 
    can be associated with an intention)
    
    Attributes:
        learning_intention:     ForeignKey to parent
        criterion_text:         Actual text of the criterion

    """
    
    learning_intention = models.ForeignKey(LearningIntention,
                                           help_text="parent learning intent"
                                           "ion for this criterion")
    criterion_text = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "criteria"
    
    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (SuccessCriterion, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            assert self.learning_intention
            assert self.criterion_text        

    def __unicode__(self):
        return self.criterion_text
        
    def __str__(self):
        """Human readable for debug mostly"""
        return "SC " + str(self.pk) + ": " + self.criterion_text
          

class LearningOutcome(models.Model):
    """The capacity or skill which is to be enhanced or acquired
    
    As distinct from the LI, LOs define a capacity which the student should
    acquire after completing the lesson (once or more times).
    The success criteria should help students determine when they have gained
    the skill specified. Essentially this is an "I can... statement"
    
    Attributes:
        learning_intention:     ForeignKey to parent
        lo_text:           Actual text of the learning outcome
    
    """
    
    learning_intention = models.ForeignKey(LearningIntention,
                                           help_text="parent learning intent"
                                           "ion for this outcome")
    lo_text = models.CharField(max_length=200)    
    
    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (LearningOutcome, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            assert self.learning_intention
            assert self.lo_text          
        
    def __unicode__(self):
        return self.lo_text
        
    def __str__(self):
        """Human readable for debug mostly"""
        return "LO " + str(self.pk) + ": " + self.lo_text        
        
        
#########################################
#Table join classes, i.e. intermediary models
#########################################

class UserProfile_Lesson(models.Model):
    """Store data relating to a user's interaction with a lesson.
    
    Attributes:
        userprofile     ForeignKey - the django user object
        lesson          ForeignKey - a lesson the user interacted with
        mark_complete   True if this lesson has been 'completed' in some way
        date_complete   Date on which lesson marked complete.
        
    """
    
#TODO create a method to set date_complete automatically when mark_complete 
#is set True.
    userprofile = models.ForeignKey(User)
    lesson = models.ForeignKey(Lesson)
    mark_complete = models.BooleanField(default=False,
                                        help_text="true if the lesson is "
                                        "'complete'")
    date_complete = models.DateField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (UserProfile_Lesson, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            assert self.userprofile
            assert self.lesson
        
    def __unicode__(self):
        assert self.userprofile
        assert self.lesson
        human_readable = str(self.userprofile) + "-" + str(self.lesson)
        return human_readable
        