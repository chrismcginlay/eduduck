import json
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import models

from django.contrib.auth.models import User

from courses.models import Course

import pdb 

class UCActions:
    """Enumeration of actions
    
    REG.    User is registering
    ACT.    User becomes active on course
    WIT.    User withdraws from course
    COM.    User completes the course
    DEA.    User becomes inactive (e.g withdraw, complete)
    REO.    User reopens course
    """
    
    [REGISTRATION, ACTIVATION, WITHDRAWAL, COMPLETION, 
     DEACTIVATION, REOPENING] = range(1,7)

    
class UserCourse(models.Model):
    """Track users interactions with courses.

    On signing up for a course and entry will be recorded here. The user may be 
    active or not (ie. maybe not seen for a while). They may complete or 
    withdraw in which case they cannot be active.
    
    Attributes:
        course
        user
        active      User is actively engaged on this course. T/F
        withdrawn   User withdrew after registration, prior to completion. T/F
        completed   User marked course complete. 
        history     History list of tuples of (datetime, action) taken 
                    eg register/complete/withdraw/reopen). Order by date.

    Methods:
        register    Create initial entry (check !exists)
        withdraw
        complete
        reopen
    """
    
    course = models.ForeignKey(Course, 
        help_text="Course user is referring to")
    user = models.ForeignKey(User, 
        help_text="User interacting with course")
    active = models.BooleanField(default=True)
    withdrawn = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    history = models.TextField(null=True, blank=True)    
    
    class Meta:
        unique_together = ('course', 'user')
       
    def _checkrep(self):
        """Verify consistency of attributes"""
#TODO   This is basic. Need to do more, eg. look at action history list to see attributes are consistent with last action.

        count = 0                
        if self.active:
            count += 1
        if self.completed:
            count += 1
        if self.withdrawn:
            count += 1
        if count > 1:
            return False
        return True
            
            
    def register(self):
        """Add new row (user,course) should be unique. This corresponds to
        a new registration on a course"""
        
        registration = UserCourse.objects.get(user=self.user, course=self.course)
        assert not(registration)   #It should not exist.
        assert self.user
        assert self.course
                
        registration = UserCourse.create(self.user, self.course)
        
        #Below, hist is a (initially empty) list of (datetime, action) tuples
#        hist = json.JSONDecoder(registration.history).skipkeys
#        hist.append((datetime.now(), UCActions.REGISTRATION))
#        registration.active = True
#        hist.append((datetime.now(), UCActions.ACTIVATION))
#        registration.history = json.JSONEncoder(hist)       
#        registration.save()
        
        assert registration._checkrep()
        return True

    def withdraw(self):
        """If not completed or already withdraw, set withdrawn."""
   
        assert self._checkrep()
        
        if self.completed:
            raise ValidationError(u'Cannot withdraw from completed course')
        if self.withdraw:
            raise ValidationError(u'Already withdrawn from this course')
        self.active = False
        self.withdrawn = True
        #Below, hist is a (initially empty) list of (datetime, action) tuples
        hist = json.JSONDecoder(self.history).skipkeys
        hist.append((datetime.now(), UCActions.DEACTIVATION))
        hist.append((datetime.now(), UCActions.WITHDRAWAL))
        self.history = json.JSONEncoder(hist)
        self.save()
        assert self._checkrep()

    def complete(self):
        """If not already completed set complete, deactivate"""
   
        assert self._checkrep()
        
        if self.completed:
            raise ValidationError(u'Already marked this course as complete')
        if self.withdraw:
            raise ValidationError(u'Cannot mark this course as complete, '\
                'because you have withdrawn from it')
        self.active = False
        self.completed = True
        #Below, hist is a (initially empty) list of (datetime, action) tuples
        hist = json.JSONDecoder(self.history).skipkeys
        hist.append((datetime.now(), UCActions.DEACTIVATION))
        hist.append((datetime.now(), UCActions.COMPLETION))
        self.history = json.JSONEncoder(hist)
        self.save()
        assert self._checkrep()

    def reopen(self):
        """Re-open a course if already withdrawn or completed"""
   
        assert self._checkrep()
        
        if not(self.completed or self.withdrawn):
            raise ValidationError(u'You can only re-open if withdrawn '\
                'or complete')
        self.active = True
        self.completed = False
        self.withdrawn = False
        #Below, hist is a (initially empty) list of (datetime, action) tuples
        hist = json.JSONDecoder(self.history).skipkeys
        hist.append((datetime.now(), UCActions.REOPENING))
        hist.append((datetime.now(), UCActions.ACTIVATION))
        self.history = json.JSONEncoder(hist)
        self.save()
        assert self._checkrep()

    def __init__(self, *args, **kwargs):
        """Run _checkrep on instantiation"""
        super (UserCourse, self).__init__(*args, **kwargs)

        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            self._checkrep()
 
    def save(self, *args, **kwargs):
        """Perform history save steps"""
        existing_row = self.pk
        super(UserCourse, self).save(*args, **kwargs)
        if not existing_row:
            hist = []
            hist.append((datetime.now(), UCActions.REGISTRATION))
            hist.append((datetime.now(), UCActions.ACTIVATION))
            self.history = json.JSONEncoder(hist)
        

    def __unicode__(self):
        return u"User " + self.user.username + \
            u"'s registration data for course:" + self.course.course_name
    
    @models.permalink
    def get_absolute_url(self):
        assert self.id >=1
        return ('interaction.views.usercourse', [str(self.id)])
                