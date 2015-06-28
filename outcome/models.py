#outcome/models.py
from django.core.urlresolvers import reverse
from django.db import models

from lesson.models import Lesson

from core.eduduck_exceptions import CheckRepError

import logging


logger = logging.getLogger(__name__)

class LearningIntention(models.Model):
    """Link Learning Intentions with individual lessons.
    
    Learning Intention: Specific learning to take place - 
    what you intend to do, e.g. practise using Newton's 2nd Law to predict
    motion of a vehicle.
    
    Attributes:
        lesson      ForeignKey to parent lesson.
        text        Actual text content of the learning intention.
        
    """
    
    lesson = models.ForeignKey(Lesson,
                               help_text="parent lesson for this intention")
    text = models.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (LearningIntention, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            self._checkrep()

    def _checkrep(self):
        if not self.lesson:
            logger.error("Learning Intention has no lesson")
            raise(CheckRepError)
        if not self.text:
            logger.warn("Learning Intention has no text content")
            return False
        return True 

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
        return self.text
        
    def __str__(self):
        """Human readable for debug mostly"""
        return "LI " + str(self.pk) + ": " + self.text
        
    def get_absolute_url(self):
        assert self.lesson
        assert self.id
        return reverse(u"outcome.views.learning_intention", kwargs = {
                'lesson_id': self.lesson.id,
                'learning_intention_id': self.id })
              
              
class LearningIntentionDetail(models.Model):
    """Learning intention details link back to individual Learning Intentions
    
    A learning intention detail can be either a success criterion or a learning
    outcome.
    Learning outcome: a capacity or skill that is to be enhanced or acquired
    Success criterion: activities demonstrating mastery of learning outcomes.
    The success criteria should help students determine when they have gained
    the skill specified. Essentially these are "I can..." statements.
    
    Attributes:
        learning_intention:     ForeignKey to parent
        text:                   Actual text of the learning intention detail
        lid_type:               Choice of either SC or LO

    """
    
    SUCCESS_CRITERION = u'SC'
    LEARNING_OUTCOME = u'LO'
    LID_DETAIL_CHOICES = (
        (SUCCESS_CRITERION, 'Success Criterion'),
        (LEARNING_OUTCOME, 'Learning Outcome')
    )
    learning_intention = models.ForeignKey(LearningIntention,
                                           help_text="parent learning intent"
                                           "ion for this criterion")
    text = models.CharField(max_length=200)
    lid_type = models.CharField(max_length=2, choices=LID_DETAIL_CHOICES)

    class Meta:
        verbose_name = "learning intention detail"
        
    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (LearningIntentionDetail, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            self._checkrep()

    def _checkrep(self):
        if not self.learning_intention:
            logger.error("LID {0} has no parent learning intention".format(
                self.pk))
            raise(CheckRepError)
        if not self.text:
            logger.warn("Recording LID {0} with no text detail".format(
                self.pk))
            return False
        if not any(self.lid_type in lid for lid in self.LID_DETAIL_CHOICES):
            logger.warn("LID {0} has invalid type".format(self.pk))
            raise(CheckRepError) 
        return True
    
    def save(self, *args, **kwargs):
        self._checkrep()
        super(LearningIntentionDetail, self).save(*args, **kwargs)    

    def __unicode__(self):
        return self.text
        
    def __str__(self):
        """Human readable for debug mostly"""
        return self.lid_type + ": " + str(self.pk) + ": " + self.text
