import json
from datetime import datetime, timedelta
from time import mktime
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

from courses.models import Course, Lesson
from outcome.models import SuccessCriteria

import pdb 
import logging
logger = logging.getLogger(__name__)

class Enum(tuple): __getattr__ = tuple.index

#Actions for UserCourse
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
            logger.error("UC Checkrep failed")
            return False
        
        #Second, compare action history with attributes
        decoded_history = self.hist2list()
        last = decoded_history.pop()
        last2 = decoded_history.pop()
        
        if self.active:
            if last[1] != 'ACTIVATION':
                logger.error("UC Checkrep failed")
                return False
            if last2[1] != 'REGISTRATION' and last2[1] != 'REOPENING':
                logger.error("UC Checkrep failed")
                return False
                
        if self.withdrawn:
            if last[1] != 'DEACTIVATION' or last2[1] != 'WITHDRAWAL':
                logger.error("UC Checkrep failed")
                return False
                
        if self.completed:
            if last[1] != 'DEACTIVATION' or last2[1] != 'COMPLETION':
                logger.error("UC Checkrep failed")
                return False       
        
        return True
             
    def hist2list(self):
        """Convert the JSON coded text in self.history to a list of tuples
        of the form (datetime, action)"""
        
        assert(self.history)
        logger.info("User:"+str(self.user.pk)+",Course:"+str(self.course.pk)+" load history")
        history = json.loads(self.history)
        list_tuple_hist = []
        for row in history:
            list_tuple_hist.append((
                datetime.fromtimestamp(row[0]), UCActions[row[1]]))
        return list_tuple_hist
               
    def withdraw(self):
        """If not completed or already withdraw, set withdrawn."""
   
        assert self._checkrep()
        logger.info("User:"+str(self.user.pk)+",Course:"+str(self.course.pk)+" withdrawal")
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
        logger.info("User:"+str(self.user.pk)+",Course:"+str(self.course.pk)+" completion")
       
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
        logger.info("User:"+str(self.user.pk)+",Course:"+str(self.course.pk)+" reopening")

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
        
    def get_status(self):
        """Return status string for human consumption"""
        
        if self.active: return 'active'
        if self.withdrawn: return 'withdrawn'
        if self.completed: return 'completed'
        assert(False, "Invalid status")

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
            logger.info("User:"+str(self.user.pk)+",Course:"+str(self.course.pk)+" registration")
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
                
#Actions for UserLesson
ULActions = Enum([
    'VISITING',
    'COMPLETING',
    'REOPENING',
])

class UserLesson(models.Model):
    """Track users interactions with lessons.
    
    Visits to lesson pages will be recorded here. A lesson may be marked as
    having been completed
    
    Attributes:
        lesson
        user
        visited     User has visited this lesson page
        completed   Lesson marked complete. 
        history     History list (datetime, action) taken. JSON coded. 
                    eg visit/complete/reopen). Order by date.
        note        Text comment area

    Methods:
        save        Overrides base class save. For new row, 
                    creates JSON coded history entries.
        visit       User visits lesson page
        complete    User completes lesson page
        reopen      User decides they need more work on this lesson
        
    Helper Methods:
        hist2list  Convert the JSON history to a list of (date, action) tuples
    """
    
    lesson = models.ForeignKey(Lesson, 
        help_text="Lesson user is interacting with")
    user = models.ForeignKey(User, 
        help_text="User interacting with course")
    visited = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    history = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ('lesson', 'user')
       
    def _checkrep(self):
        """Verify consistency of attributes and history"""

        #First, basic attributes.
        if self.completed and not self.visited:
            logger.error("UL Checkrep failed")
            return False
        
        #Second, compare action history with attributes
        decoded_history = self.hist2list()
        first = decoded_history[0]
        
        #If VISITING is the first history event then visited should be true
        #and vice-versa.
        if self.visited:
            if first[1] != 'VISITING':
                logger.error("UL Checkrep failed")
                return False
        if first[1] == 'VISITING':
            if self.visited == False:
                logger.error("UL Checkrep failed")
                return False
        #if the last history event is 'COMPLETING' then completed should be true
        last = decoded_history.pop()
        if last[1] == 'COMPLETING':
            if self.completed == False:
                logger.error("UL Checkrep failed")
                return False
        
        #history events should be a member of the set 
        #[VISITING, COMPLETING, REOPENING]
        for event in decoded_history:
            if event[1] not in ULActions:
                logger.error("UL Checkrep failed")
                return False
        
        return True
             
    def hist2list(self):
        """Convert the JSON coded text in self.history to a list of tuples
        of the form (datetime, action)"""
        
        assert(self.history)
        logger.info("User:"+str(self.user.pk)+",Lesson:"+str(self.lesson.pk)+" load history")
        history = json.loads(self.history)
        list_tuple_hist = []
        for row in history:
            list_tuple_hist.append((
                datetime.fromtimestamp(row[0]), ULActions[row[1]]))
        return list_tuple_hist
    
    def visit(self):
        """Mark lesson as visited"""
        
        assert self._checkrep()
        course_record = self.user.usercourse_set.get(course=self.lesson.course)
        #view should not try to record lesson unless registered on course
        assert(course_record)

        logger.info("User:"+str(self.user.pk)+",Lesson:"+str(self.lesson.pk)+" visiting")
        self.visited = True
        hist = json.loads(self.history)
        current_time = mktime(datetime.now().utctimetuple())
        hist.append((current_time, ULActions.VISITING))
        self.history = json.dumps(hist)
        self.save()
        assert self._checkrep()
        
    def complete(self):
        """If not already completed set complete"""
   
        assert self._checkrep()
        logger.info("User:"+str(self.user.pk)+",Lesson:"+str(self.lesson.pk)+" completion")
       
        if self.completed:
            raise ValidationError(u'Already marked this lesson as complete')
        self.completed = True
        hist = json.loads(self.history)
        current_time = mktime(datetime.now().utctimetuple())
        hist.append((current_time, ULActions.COMPLETING))
        self.history = json.dumps(hist)
        self.save()
        assert self._checkrep()

    def reopen(self):
        """User may mark a lesson as not complete, only if already completed"""
   
        assert self._checkrep()
        logger.info("User:"+str(self.user.pk)+",Lesson:"+str(self.lesson.pk)+" reopening")

        if not self.completed:
            raise ValidationError(u'You can only re-open or complete')
        self.completed = False
        hist = json.loads(self.history)
        current_time = mktime(datetime.now().utctimetuple())
        hist.append((current_time, ULActions.REOPENING))
        self.history = json.dumps(hist)
        self.save()
        assert self._checkrep()
        
    def get_status(self):
        """Return status string for human consumption"""
        
        #test completed first, as that will eclipse visited status.
        if self.completed: return 'completed'
        elif self.visited: return 'visited'
        else: return 'not visited'

    def __init__(self, *args, **kwargs):
        """Run _checkrep on instantiation"""
        super (UserLesson, self).__init__(*args, **kwargs)

        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            self._checkrep()
 
    def save(self, *args, **kwargs):
        """Perform history save steps"""
        
        existing_row = self.pk
        super(UserLesson, self).save(*args, **kwargs)
        if not existing_row:
            course_record = self.user.usercourse_set.get(course=self.lesson.course)
            #view should not try to record lesson unless registered on course
            assert(course_record)
            logger.info("User:"+str(self.user.pk)+",Lesson:"+str(self.lesson.pk)+" first visit")
            hist = []
            current_time = mktime(datetime.now().utctimetuple())
            hist.append((current_time, ULActions.VISITING))
            self.history = json.dumps(hist)
            self.visited = True
            self.save()

    def __str__(self):
        """Human readable summary"""
        
        return u"User " + self.user.username + \
            u"'s data for lesson:" + self.lesson.lesson_name
            
    def __unicode__(self):
        """Summary for internal use"""
        
        return u"UL:%s, User:%s, Lesson:%s" % \
            (self.pk, self.user.pk, self.lesson.pk)
    
    @models.permalink
    def get_absolute_url(self):
        assert self.id
        assert self.lesson
        assert self.user
        
        return ('interaction.views.userlesson_single', (), {
            'user_id': self.user.pk,
            'lesson_id': self.lesson.pk })

#Actions for Outcomes (learning outcomes and success criteria)
UOActions = Enum([
    'MARKING_RED',
    'MARKING_AMBER',
    'MARKING_GREEN'
])

UOConditions = Enum(['red', 'amber', 'green'])

class UserSuccessCriteria(models.Model):
    """Track user interactions with success criteria
    
    Marking the 'traffic light' widgets as red/amber/green will require to be 
    recorded in the database.
    
    Attributes:
        success_criterion   
        user
        condition           0=red, 1=amber, or 2=green
        history
        
    Methods:
        save        Overrides base class save. For new row
                    creates JSON coded history entry.
        cycle       Cycle attribute red->amber->green->red
        
    Helper Methods:
        hist2list   Convert JSON history to a list of (date, action) tuples
    """
    
    user = models.ForeignKey(User, help_text="User interacting with criteria")
    success_criterion = models.ForeignKey(SuccessCriteria, 
        help_text="Criterion user is interacting with")
    condition = models.SmallIntegerField(default=UOConditions.red)
    history = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'success_criterion')
    
    def _checkrep(self):
        """Verify internal consistency of attributes and history"""
        
        if self.condition not in UOConditions:
            logger.error("UO Checkrep detected errored state")
            return False
            
        #compare history with state
        decoded_history = self.hist2list()
        last = decoded_history.pop()
        
        if self.condition == UOConditions.red:
            if last[1] != UOActions.MARKING_RED:
                logger.error("UO Checkrep detected errored state")
                return False
        elif self.condition == UOConditions.amber:
            if last[1] != UOActions.MARKING_AMBER:
                logger.error("UO Checkrep detected errored state")
                return False
        elif self.condition == UOConditions.green:
            if last[1] != UOActions.MARKING_GREEN:
                logger.error("UO Checkrep detected errored state")
                return False
                
        #history events should be a member of the set 
        #UOActions
        for event in decoded_history:
            if event[1] not in UOActions:
                logger.error("UL Checkrep failed")
                return False    
        
        return True
      
      
    def save(self, *args, **kwargs):
        """Perform history save steps"""
        
        existing_row = self.pk
        super(UserSuccessCriteria, self).save(*args, **kwargs)
        if not existing_row:
            course_record = self.user.usercourse_set.get(course=self.lesson.course)
            #view should not try to record lesson unless registered on course
            assert(course_record)
            logger.info("User:"+str(self.user.pk)+",SC:"+str(self.success_criterion.pk)+" first visit")
            hist = []
            current_time = mktime(datetime.now().utctimetuple())
            pdb.set_trace() #TODO verify marking behaviour
            hist.append((current_time, UOActions.MARKING_AMBER))
            self.history = json.dumps(hist)
            self.visited = True
            self.save()
            
            
    def hist2list(self):
        """Convert the JSON coded text in self.history to a list of tuples
        of the form (datetime, action)"""
        
        assert self.history
        logger.info("User:"+str(self.user.pk)+",SC:"+str(self.success_criteria.pk)+" load history")
        history = json.loads(self.history)
        list_tuple_hist = []
        for row in history:
            list_tuple_hist.append((
                datetime.fromtimestamp(row[0]), UOActions[row[1]]))
        return list_tuple_hist
        
    def cycle(self):
        """3-state cyclic permutation of rag state"""
        
        assert self._checkrep()
        logger.info("User:"+str(self.user.pk)+",SC:"+str(self.success_criterion.pk)+" cycling")
        hist = self.hist2list()
        last_event = hist[:1]
        event_date = last_event[0]
        #don't wish to flood history if user clicks endlessly. Store only the
        #final state within the last 5 minute time period.
        pdb.set_trace()        
        if self.condition == 0:
            action = UOActions.SET_AMBER
        elif self.condition == 1:
            action = UOActions.SET_GREEN
        elif self.condition == 2:
            action = UOActions.SET_RED
        else:
            raise ValueError
        current_time = mktime(datetime.now().utctimetuple())
        if (current_time - event_date) > timedelta(mins = 5):
            #over 5 mins elapsed: add to the history
            hist.append((current_time, action))
        else:
            #under 5 mins elapsed: replace the last history event
            hist.pop()
            hist.append((current_time, action))
            
        if self.condition < 2:
            self.condition += 1
        else:
            self.condition = 0
            
        self.save()            
        assert self._checkrep()