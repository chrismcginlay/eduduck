from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

#TODO implement get_absolute_url() methods

class Course(models.Model):
    #abbreviated course code
    course_code = models.CharField(max_length=10)

    #full name of course
    course_name = models.CharField(max_length=150)
    
    #summary paragraph of course
    course_abstract = models.TextField()

    #name of person responsible for course
    course_organiser = models.CharField(max_length=100)

    #some scheme of level of advancement/difficulty
    course_level = models.CharField(max_length=10, blank=True, null=True)
    
    #number of credit points awarded on completion
    course_credits = models.IntegerField(blank=True, null=True)
    
    #attachments held in Foreign Key with attachment class
    #intro video held in Video class
    
    def __unicode__(self):
        return self.course_name
        
class Lesson(models.Model):
    #Human readable abbreviated lesson name
    lesson_code = models.CharField(max_length=10, blank=True, null=True)
    lesson_name = models.CharField(max_length=200)
    
    #course to which lesson belongs
    course = models.ForeignKey(Course)
    
    #short text description of the lesson
    abstract = models.TextField()

    def get_next(self):
        '''Return the next lesson in the course'''
        next = Lesson.objects.filter(id__gt=self.id)
        if next:
            return next[0]
        return False
        
    def get_prev(self):
        '''Return the previous lesson in the course'''
        prev = Lesson.objects.filter(id__lt=self.id)
        if prev:
            return prev[0]
        return False
    
    def __unicode__(self):
        return self.lesson_name
        
class Video(models.Model):
    #TODO: use YouTube / Vimeo APIs to pull video meta data such as title, tags    
    
    #Human readable abbreviated video name
    video_code = models.CharField(max_length=10, blank=True, null=True)
    video_name = models.CharField(max_length=200)
    url = models.URLField()
    
    #video may belong to lesson or directly to course.
    lesson = models.ForeignKey(Lesson, blank=True, null=True)
    course = models.ForeignKey(Course, blank=True, null=True)
    
    def __unicode__(self):
        return self.video_name
        
class Attachments(models.Model):
    '''Handle all forms of attachment except video'''
    #TODO: better modules exist for this.
    #TODO: remove plural from this class name, not consistent!
    
    #Human readable abbreviated name and name
    att_code = models.CharField(max_length=10, blank=True, null=True)
    att_name = models.CharField(max_length=200)
    
    #attachment may belong to a lesson or directly to course
    #TODO insist precisely one of the following is valid.
    lesson = models.ForeignKey(Lesson, blank=True, null=True)
    course = models.ForeignKey(Course, blank=True, null=True)
    
    #Optional description of attachment
    att_desc = models.TextField(blank=True, null=True)
    #Optional sequence number of attachment
    att_seq = models.IntegerField(blank=True, null=True)
    
    #local filesystem URL
    att_url = models.URLField()
    
    def __unicode__(self):
        return self.att_name
        
#Based on section 3.10 of PDF manual
class UserProfile(models.Model):
    '''Extend User module with additional data'''
    #required field
    user = models.OneToOneField(User)
    
    lessons = models.ManyToManyField(Lesson, through='UserProfile_Lesson')
    accepted_terms = models.BooleanField()
    signature_line = models.CharField(max_length=200)
    registered_courses = models.ManyToManyField(Course)
    
    def __unicode__(self):
        return self.user.username
        
# extraneous: implemented in User class
#    def __unicode__(self):
#       return self.user.username

#########################################
#Table join classes, i.e. intermediary models
#########################################

class UserProfile_Lesson(models.Model):
    '''Store data relating to a user's interaction with a lesson'''
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
    '''Ensure user profile is created for each new user'''
    if created:
        UserProfile.objects.create(user=instance)

#Register to receive the signal
#post_save.connect(create_user_profile, sender=User)