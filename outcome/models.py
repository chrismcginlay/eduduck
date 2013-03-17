from django.db import models
from courses.models import Lesson

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
        return ('views.learning_intention', (), {
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