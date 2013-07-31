from django.db import models
from courses.models import Lesson

import pdb

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
            assert self.lesson
            assert self.text

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
        
    @models.permalink
    def get_absolute_url(self):
        assert self.lesson
        assert self.id
        return ('outcome.views.learning_intention', (), {
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
        type:                   Choice of either SC or LO

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
    type = models.CharField(max_length=2, choices=LID_DETAIL_CHOICES)

    class Meta:
        verbose_name = "learning intention detail"
        
    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (LearningIntentionDetail, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            assert self.learning_intention
            assert self.text
            assert self.type

    def __unicode__(self):
        return self.text
        
    def __str__(self):
        """Human readable for debug mostly"""
        return self.type + ": " + str(self.pk) + ": " + self.text
