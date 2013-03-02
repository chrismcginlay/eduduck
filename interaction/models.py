import json
from datetime import datetime
from time import mktime
from django.core.exceptions import ValidationError
from django.db import models

from django.contrib.auth.models import User

from courses.models import Course

import pdb 

class Enum(tuple): __getattr__ = tuple.index

UCActions = Enum([
    'REGISTRATION',
    'ACTIVATION', 
    'WITHDRAWAL', 
    'COMPLETION',
    'DEACTIVATION',
    'REOPENING',
    ])

    
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
        history     History list (datetime, action) taken. JSON coded. 
                    eg register/complete/withdraw/reopen). Order by date.

    Methods:
        save        Overrides base class save. For new row, 
                    creates JSON coded history entries.
        withdraw
        complete
        reopen
        
    Helper Methods:
        hist2list  Convert the JSON history to a list of (date, action) tuples
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
        """Verify consistency of attributes and history"""

        #First, basic attributes.
        count = 0                
        if self.active:
            count += 1
        if self.completed:
            count += 1
        if self.withdrawn:
            count += 1
        if count != 1:
            return False
        
        #Second, compare action history with attributes
        decoded_history = self.hist2list()
        last = decoded_history.pop()
        last2 = decoded_history.pop()
        
        if self.active:
            if last[1] != 'ACTIVATION':
                return False
            if last2[1] != 'REGISTRATION' and last2[1] != 'REOPENING':
                return False
                
        if self.withdrawn:
            if last[1] != 'DEACTIVATION' or last2[1] != 'WITHDRAWAL':
                return False
                
        if self.completed:
            if last[1] != 'DEACTIVATION' or last2[1] != 'COMPLETION':
                return False       
        
        return True
             
    def hist2list(self):
        """Convert the JSON coded text in self.history to a list of tuples
        of the form (datetime, action)"""
        
        assert(self.history)
        history = json.loads(self.history)
        list_tuple_hist = []
        for row in history:
            list_tuple_hist.append((
                datetime.fromtimestamp(row[0]), UCActions[row[1]]))
        return list_tuple_hist
        
    def withdraw(self):
        """If not completed or already withdraw, set withdrawn."""
   
        assert self._checkrep()
        
        if self.completed:
            raise ValidationError(u'Cannot withdraw from completed course')
        if self.withdrawn:
            raise ValidationError(u'Already withdrawn from this course')
        self.active = False
        self.withdrawn = True
        hist = json.loads(self.history)
        current_time = mktime(datetime.now().utctimetuple())
        hist = json.loads(self.history)
        hist.append((current_time, UCActions.WITHDRAWAL))
        hist.append((current_time, UCActions.DEACTIVATION))
        self.history = json.dumps(hist)
        self.save()
        assert self._checkrep()

    def complete(self):
        """If not already completed set complete, deactivate"""
   
        assert self._checkrep()
        
        if self.completed:
            raise ValidationError(u'Already marked this course as complete')
        if self.withdrawn:
            raise ValidationError(u'Cannot mark this course as complete, '\
                'because you have withdrawn from it')
        self.active = False
        self.completed = True
        hist = json.loads(self.history)
        current_time = mktime(datetime.now().utctimetuple())
        hist.append((current_time, UCActions.COMPLETION))
        hist.append((current_time, UCActions.DEACTIVATION))
        self.history = json.dumps(hist)
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
        hist = json.loads(self.history)
        current_time = mktime(datetime.now().utctimetuple())
        hist.append((current_time, UCActions.REOPENING))
        hist.append((current_time, UCActions.ACTIVATION))
        self.history = json.dumps(hist)
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
            current_time = mktime(datetime.now().utctimetuple())
            hist.append((current_time, UCActions.REGISTRATION))
            hist.append((current_time, UCActions.ACTIVATION))
            self.history = json.dumps(hist)
            self.save()

    def __str__(self):
        """Human readable summary"""
        
        return u"User " + self.user.username + \
            u"'s data for course:" + self.course.course_name
            
    def __unicode__(self):
        """Summary for internal use"""
        
        return u"UC:%s, User:%s, Course:%s" % \
            (self.pk, self.user.pk, self.course.pk)
    
    @models.permalink
    def get_absolute_url(self):
        assert self.id
        assert self.course
        assert self.user
        
        return ('interaction.views.usercourse_single', (), {
            'user_id': self.user.pk,
            'course_id': self.course.pk })
                