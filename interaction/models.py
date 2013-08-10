import json
from datetime import datetime, timedelta
from time import mktime

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.timezone import utc, is_naive
from django.db import models
from django.contrib.auth.models import User

from courses.models import Course, Lesson
from outcome.models import LearningIntention, LearningIntentionDetail
from attachment.models import Attachment

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
            logger.warning("UC _checkrep() detected errored state (could be a test?)")
            return False
        
        #Second, compare action history with attributes
        decoded_history = self.hist2list()
        last = decoded_history.pop()
        last2 = decoded_history.pop()
        
        if is_naive(last[0]):
            logger.warning("UC _checkrep() detected naive timezone (could be a test)")
            return False
        if is_naive(last2[0]):
            logger.warning("UC _checkrep() detected naive timezone (could be a test)")
            return False
            
        if self.active:
            if last[1] != 'ACTIVATION':
                logger.warning("UC _checkrep() detected errored state (could be a test?)")
                return False
            if last2[1] != 'REGISTRATION' and last2[1] != 'REOPENING':
                logger.warning("UC _checkrep() detected errored state (could be a test?)")
                return False
                
        if self.withdrawn:
            if last[1] != 'DEACTIVATION' or last2[1] != 'WITHDRAWAL':
                logger.warning("UC _checkrep() detected errored state (could be a test?)")
                return False
                
        if self.completed:
            if last[1] != 'DEACTIVATION' or last2[1] != 'COMPLETION':
                logger.warning("UC _checkrep() detected errored state (could be a test?)")
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
                datetime.utcfromtimestamp(row[0]).replace(tzinfo=utc), 
                UCActions[row[1]]))
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
        current_time = mktime(datetime.utcnow()
            .replace(tzinfo=utc)
            .utctimetuple())
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
        current_time = mktime(datetime.utcnow().replace(tzinfo=utc).utctimetuple())
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
        current_time = mktime(datetime.utcnow()
            .replace(tzinfo=utc)
            .utctimetuple())
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
            current_time = mktime(datetime.utcnow()
                .replace(tzinfo=utc)
                .utctimetuple())
            hist.append((current_time, UCActions.REGISTRATION))
            hist.append((current_time, UCActions.ACTIVATION))
            self.history = json.dumps(hist)
            self.save()

    def __str__(self):
        """Human readable summary"""
        
        return u"User " + self.user.username + \
            u"'s data for course:" + self.course.name
            
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
            logger.warning("UL _checkrep() detected errored state (could be a test?)")
            return False
        
        #Second, compare action history with attributes
        decoded_history = self.hist2list()
        first = decoded_history[0]
        
        #If VISITING is the first history event then visited should be true
        #and vice-versa.
        if self.visited:
            if first[1] != 'VISITING':
                logger.warning("UL _checkrep() detected errored state (could be a test?)")
                return False
        if first[1] == 'VISITING':
            if self.visited == False:
                logger.warning("UL _checkrep() detected errored state (could be a test?)")
                return False
        #if the last history event is 'COMPLETING' then completed should be true
        last = decoded_history.pop()
        if last[1] == 'COMPLETING':
            if self.completed == False:
                logger.warning("UL _checkrep() detected errored state (could be a test?)")
                return False
        
        #history events should be a member of the set 
        #[VISITING, COMPLETING, REOPENING]
        #Datetimes should be timezone aware.
        for event in decoded_history:
            if event[1] not in ULActions:
                logger.warning("UL _checkrep() detected errored state (could be a test?)")
                return False
            if is_naive(event[0]):
                logger.warning("UL _checkrep() detected naive timezone (could be a test)")
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
                datetime.utcfromtimestamp(row[0]).replace(tzinfo=utc), 
                ULActions[row[1]]))
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
        current_time = mktime(datetime.utcnow()
            .replace(tzinfo=utc)
            .utctimetuple())
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
        current_time = mktime(datetime.utcnow()
            .replace(tzinfo=utc)
            .utctimetuple())
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
        current_time = mktime(datetime.utcnow()
            .replace(tzinfo=utc)
            .utctimetuple())
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
            current_time = mktime(datetime.utcnow()
                .replace(tzinfo=utc)
                .utctimetuple())
            hist.append((current_time, ULActions.VISITING))
            self.history = json.dumps(hist)
            self.visited = True
            self.save()

    def __str__(self):
        """Human readable summary"""
        
        return u"User " + self.user.username + \
            u"'s data for lesson:" + self.lesson.name
            
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

class UserLearningIntention(models.Model):
    """User interaction with learning intentions
    
    Attributes:
        learning_intention
        user
        
    Methods:
        progress            return dictionary of tuples indexed via 'SC' or 'LO'
    """

    #TODO: cache the progress status in the database as it will be cheaper
    #when rendering course summaries.
    user = models.ForeignKey(User, help_text="User interacting with LI")
    learning_intention = models.ForeignKey(LearningIntention, 
        help_text=  "Learning intention user is interacting with")

    class Meta:
        unique_together =   ('user', 'learning_intention')       

    def progress(self):
        """Compute and return representation of progress through this LI"""
        
        pdict = { u'SC':None, u'LO':None }
        user_SCs = self.user.userlearningintentiondetail_set.filter(
            condition = ULIDConditions.green,
            learning_intention_detail__in = 
                self.learning_intention.learningintentiondetail_set.filter(
                    lid_type=LearningIntentionDetail.SUCCESS_CRITERION)
        ).count()
        user_LOs = self.user.userlearningintentiondetail_set.filter(
            condition = ULIDConditions.green,
            learning_intention_detail__in = 
                self.learning_intention.learningintentiondetail_set.filter(
                    lid_type=LearningIntentionDetail.LEARNING_OUTCOME)
        ).count()
        LI_SCs = self.learning_intention.learningintentiondetail_set.filter(
            lid_type = LearningIntentionDetail.SUCCESS_CRITERION).count()
        LI_LOs = self.learning_intention.learningintentiondetail_set.filter(
            lid_type = LearningIntentionDetail.LEARNING_OUTCOME).count()        
        pdict[u'SC'] = (user_SCs, LI_SCs)
        pdict[u'LO'] = (user_LOs, LI_LOs)
        return pdict
        
    def __str__(self):
        """Human readable summary"""
        
        return u"User " + self.user.username + \
            u"'s data for LI:" + \
            self.learning_intention.text[:10] + "..."
            
    def __unicode__(self):
        """Summary for internal use"""
        
        return u"ULI:%s, User:%s, LI:%s" % \
            (self.pk, self.user.pk, self.learning_intention.pk)
            
#Actions for Learning Intention Details(learning outcomes and success criteria)
ULIDActions = Enum([
    'SET_RED',
    'SET_AMBER',
    'SET_GREEN'
])

ULIDConditions = Enum(['red', 'amber', 'green'])

class UserLearningIntentionDetail(models.Model):
    """Track user interactions with learning intention details
    
    Marking the 'traffic light' widgets as red/amber/green will require to be 
    recorded in the database.
    
    Attributes:
        learning_intention_detail   
        user
        condition           0=red, 1=amber, or 2=green. Instance o ULIDCondition
        history
        
    Methods:
        save        Overrides base class save. For new row
                    creates JSON coded history entry.
        cycle       Cycle attribute red->amber->green->red
        
    Helper Methods:
        hist2list   Convert JSON history to a list of (date, action) tuples
    """
    
    user = models.ForeignKey(User, help_text="User interacting with LI detail")
    learning_intention_detail = models.ForeignKey(LearningIntentionDetail, 
        help_text=  "Success criterion or learning outcome user"\
        " is interacting with")
    condition = models.SmallIntegerField(default=ULIDConditions.red)
    history = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together =   ('user', 'learning_intention_detail')
        verbose_name =      "user's learning intention detail"
    
    def _checkrep(self):
        """Verify internal consistency of attributes and history"""
        
        try:
            ULIDConditions[self.condition]
        except IndexError:
            logger.warning("ULID _checkrep() detected errored state (could be a test?)")
            return False
            
        #compare history with state
        decoded_history = self.hist2list()
        last = decoded_history.pop()
        
        if self.condition == ULIDConditions.red:
            if last[1] != "SET_RED":
                logger.warning("ULID _checkrep() detected errored state (could be a test?)")
                return False
        elif self.condition == ULIDConditions.amber:
            if last[1] != "SET_AMBER":
                logger.warning("ULID _checkrep() detected errored state (could be a test?)")
                return False
        elif self.condition == ULIDConditions.green:
            if last[1] != "SET_GREEN":
                logger.warning("ULID _checkrep() detected errored state (could be a test?)")
                return False
                
        #history events should be a member of the set ULIDActions
        #and datestamps should be timezone aware
        for event in decoded_history:
            if event[1] not in ULIDActions:
                logger.warning("ULID _checkrep() detected errored state (could be a test?)")
                return False    
            if is_naive(event[0]):
                logger.warning("ULID _checkrep() detected naive timezone (could be a test)")
                return False        
        return True
      
      
    def save(self, *args, **kwargs):
        """Perform history save steps"""
        
        existing_row = self.pk
        super(UserLearningIntentionDetail, self).save(*args, **kwargs)
        if not existing_row:
            #a long and winding ORM hop.
            usercourse = self.learning_intention_detail.learning_intention.lesson.course
            course_record = self.user.usercourse_set.get(course=usercourse)
            #view should not try to record lesson unless registered on course
            assert(course_record)
            logger.info("User:"+str(self.user.pk)+",LID:"+\
                str(self.learning_intention_detail.pk)+" first visit")
            hist = []
            current_time = mktime(datetime.utcnow()
                .replace(tzinfo=utc)
                .utctimetuple())
            hist.append((current_time, ULIDActions.SET_RED))
            self.history = json.dumps(hist)
            self.condition = ULIDConditions.red
            self.save()
            
            
    def hist2list(self):
        """Convert the JSON coded text in self.history to a list of tuples
        of the form (datetime, action)"""
        
        assert self.history
        logger.info("User:"+str(self.user.pk)+",LID:"+\
                str(self.learning_intention_detail.pk)+" load history")
        history = json.loads(self.history)
        list_tuple_hist = []
        for row in history:
            list_tuple_hist.append((
                datetime.utcfromtimestamp(row[0]).replace(tzinfo=utc), 
                ULIDActions[row[1]]))
        return list_tuple_hist
        
    def cycle(self):
        """3-state cyclic permutation of RAG state"""

        assert self._checkrep()
        logger.info("User:"+str(self.user.pk)+",SC:"+\
                str(self.learning_intention_detail.pk)+" cycling")
        hist = json.loads(self.history)
        last_event = hist[-1]    #slice, last element only, (its a tuple)
        event_date = last_event[0]  #datetime part of the tuple
        #don't wish to flood history if user clicks endlessly. Store only the
        #final state within the last 5 minute time period.
     
        if self.condition == ULIDConditions.red:
            action = ULIDActions.SET_AMBER
        elif self.condition == ULIDConditions.amber:
            action = ULIDActions.SET_GREEN
        elif self.condition == ULIDConditions.green:
            action = ULIDActions.SET_RED
        else:
            raise ValueError

        #check elapsed time using utc
        current_time = datetime.utcnow().replace(tzinfo=utc)
        event_time = datetime.utcfromtimestamp(event_date).replace(tzinfo=utc)
        if (current_time - event_time) < timedelta(minutes = 5):
            #under 5 mins elapsed: replace the last history event
            hist.pop()

        serial_time = mktime(current_time.utctimetuple())
        hist.append((serial_time, action))
            
        if self.condition < 2:
            self.condition += 1
        else:
            self.condition = 0
        
        self.history = json.dumps(hist)
        self.save()            
        assert self._checkrep()
        
        
    def __str__(self):
        """Human readable summary"""
        
        return u"User " + self.user.username + u"'s data for LID:" + \
            self.learning_intention_detail.text[:10] + "..."

    def __unicode__(self):
        """Summary for internal use"""
        
        return u"ULID:%s, User:%s, LID:%s" % \
            (self.pk, self.user.pk, self.learning_intention_detail.pk)
            
    
    def get_status(self):
        """Return status string for human consumption"""
    
        return ULIDConditions[self.condition]
        
#Actions for UserAttachment
UAActions = Enum([
    'DOWNLOADING',
    ])

class UserAttachment(models.Model):
    """Track users interactions with attachments.
    
    Downloaded attachments will be recorded here.
    
    Attributes:
        attachment
        user
        history     History list (datetime, action). JSON coded, date ordered

    Methods:
        save        Overrides base class save. For new row, 
                    creates JSON coded history entries.
        record_download    Record a user download of attachment
        
    Helper Methods:
        hist2list  Convert the JSON history to a list of (date, action) tuples
    """
    
    attachment = models.ForeignKey(Attachment, 
        help_text="attachment user is downloading")
    user = models.ForeignKey(User, 
        help_text="User interacting with attachment")
    history = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ('attachment', 'user')
       
    def _checkrep(self):
        """Verify consistency of attributes and history"""
        
        #Verify action history
        decoded_history = self.hist2list()
        for event in decoded_history:
            if event[1] not in UAActions:
                logger.warning("""UA _checkrep() detected errored state\
                    (could be a test?)""")
                return False
            if is_naive(event[0]):
                logger.warning("""UA _checkrep() detected naive timezone\
                    (could be a test?)""")
                return False   
        return True
             
    def hist2list(self):
        """Convert the JSON coded text in self.history to a list of tuples
        of the form (datetime, action)"""
        
        assert(self.history)
        logger.info("UA: %s, User: %s, Attachment: %s loading history" %\
            (self.pk, self.user.pk, self.attachment.pk))
        history = json.loads(self.history)
        list_tuple_hist = []
        for row in history:
            list_tuple_hist.append((
                datetime.utcfromtimestamp(row[0]).replace(tzinfo=utc), 
                UAActions[row[1]]))
        return list_tuple_hist
        
    def record_download(self):
        """Add record of download to history"""
        
        assert self._checkrep()
        logger.info("UA: %s, User: %s, Attachment: %s download." %\
            (self.pk, self.user.pk, self.attachment.pk))
        hist = json.loads(self.history)
        current_time = mktime(datetime.utcnow()
            .replace(tzinfo=utc)
            .utctimetuple())
        hist.append((current_time, UAActions.DOWNLOADING))
        self.history = json.dumps(hist)
        self.save()
        assert self._checkrep()
            
    def __init__(self, *args, **kwargs):
        """Run _checkrep on instantiation"""
        super (UserAttachment, self).__init__(*args, **kwargs)

        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            self._checkrep()
 
    def save(self, *args, **kwargs):
        """Perform history save steps"""
        
        existing_row = self.pk
        super(UserAttachment, self).save(*args, **kwargs)
        if not existing_row:
            #Model should not try to record download unless user is 
            #registered on relevant course. Attachment can be linked to course
            #or to individual lesson, either way, we need to get to the course
            try:
                course_record = self.user.usercourse_set.get(course=self.attachment.course)
            except ObjectDoesNotExist:
                try:
                    course_record = self.user.usercourse_set.get(course=self.attachment.lesson.course)
                except ObjectDoesNotExist:
                    course_record = None
            logger.info("User:"+str(self.user.pk)+",Attachment:"+str(self.attachment.pk)+" download")
            if course_record:
                hist = []
                current_time = mktime(datetime.utcnow()
                    .replace(tzinfo=utc)
                    .utctimetuple())
                hist.append((current_time, UAActions.DOWNLOADING))
                self.history = json.dumps(hist)
                self.save()
            else:
                #Getting here implies no course_record. Should not be storing
                #record of interaction if user not on course
                assert(False)
                
    def __str__(self):
        """Human readable summary"""
        
        return u"User %s's data for attachment: ...%s" %\
            (self.user.username, str(self.attachment.attachment)[-10:])
            
    def __unicode__(self):
        """Summary for internal use"""
        
        return u"UA:%s, User:%s, Attachment:%s" % \
            (self.pk, self.user.pk, self.attachment.pk)
    
    def get_absolute_url(self):
        assert self.id
        assert self.attachment
        assert self.user

        return reverse(u"interaction.views.attachment_download",
                       kwargs= {'att_id': self.attachment.pk})
        
