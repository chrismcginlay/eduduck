from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

#TODO implement get_absolute_url() methods

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

    course_code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=150)
    course_abstract = models.TextField()
    
    #TODO change this to ForeignKey(UserPrf)
    course_organiser = models.CharField(max_length=100)
    course_level = models.CharField(max_length=10, blank=True, null=True)
    course_credits = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return self.course_name
    
    @models.permalink
    def get_absolute_url(self):
        return ('courses.views.single', [str(self.id)])
        
class Lesson(models.Model):
    """A digestible chunk of learning material within a course.
    
    Attributes:
        lesson_code     Lesson code for human consumption
        lesson_name     Human readable full lesson name
        course          ForeignKey - course to which lesson belongs
        abstract        short text description of the lesson
        
    """
    
    lesson_code = models.CharField(max_length=10, blank=True, null=True)
    lesson_name = models.CharField(max_length=200)
    course = models.ForeignKey(Course)
    abstract = models.TextField()

    def get_next(self):
        """Return the next lesson in the course"""
        next = Lesson.objects.filter(course=self.course).filter(id__gt=self.id)
        if next:
            return next[0]
        return False
        
    def get_prev(self):
        """Return the previous lesson in the course"""
        prev = Lesson.objects.filter(course=self.course).filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev[0]
        return False
    
    def __unicode__(self):
        return self.lesson_name
    
    @models.permalink
    def get_absolute_url(self):
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
    
    def __unicode__(self):
        return self.video_name

# No video view defined yet 
#    @models.permalink
#    def get_absolute_url(self):
#        return ('TODO')
        
        
class Attachments(models.Model):
    """Handle all forms of attachment except video.
    
    Attributes:
        att_code    Attachment code for human consumption
        att_name    Human readable name of the attachment
        lesson      ForeignKey - if attachment embedded in lesson
        course      ForeignKey - if attachment embedded in course
        att_desc    Paragraph describing contents of attachment
        att_seq     Optional unique sequence number of attachment
        att_url     URL to file (local/external)

    """
    
    #TODO: better modules exist for this.
    #TODO: remove plural from this class name, not consistent!
    
    att_code = models.CharField(max_length=10, blank=True, null=True)
    att_name = models.CharField(max_length=200)
    #TODO: override __init__ to ensure precisely one of the following is not null
    lesson = models.ForeignKey(Lesson, blank=True, null=True)
    course = models.ForeignKey(Course, blank=True, null=True)
    att_desc = models.TextField(blank=True, null=True)
    att_seq = models.IntegerField(blank=True, null=True)
    att_url = models.URLField()
    
    class Meta:
        unique_together = (("lesson", "att_seq"),)   
        
    def __unicode__(self):
        return self.att_name

# No attachment view defined yet 
#    @models.permalink
#    def get_absolute_url(self):
#        return ('TODO')   


class UserProfile(models.Model):
    """Extend User module with additional data.
    
    Custom user profile data based on section 3.10 of PDF manual
    
    Attributes:
        user                1-1Field - Required field - User
        lessons             Intermediary - user interaction with lessons
        accepted_terms      Either you do or you don't
        signature_line      Personal motto for user
        registered_courses  m-mField - Courses user is registered on
    
    """
    
    user = models.OneToOneField(User)
    lessons = models.ManyToManyField(Lesson, through='UserProfile_Lesson')
    accepted_terms = models.BooleanField()
    signature_line = models.CharField(max_length=200)
    registered_courses = models.ManyToManyField(Course)
    
    def __unicode__(self):
        return self.user.username
        
    @models.permalink
    def get_absolute_url(self):
        return ('courses.views.user_profile', [str(self.id)])
        
        
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
    userprofile = models.ForeignKey(UserProfile)
    lesson = models.ForeignKey(Lesson)
    mark_complete = models.BooleanField(default=False)
    date_complete = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        human_readable = str(self.userprofile) + "-" + str(self.lesson)
        return human_readable
        
#########################################
#   Signals Area
#########################################

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Ensure user profile is created for each new user"""
    if created:
        UserProfile.objects.create(user=instance)