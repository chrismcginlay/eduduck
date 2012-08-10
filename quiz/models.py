from django.db import models
from django.contrib.auth.models import User
from courses.models import Lesson

# TODO eventually create other types of quiz, using an abstract base class
# Early days: get everything working with simple multichoice.

class Answer(models.Model):
    """Multichoice style answer. 
    
    Represent a possible answer along with explanatory text
    
    """
    
    answer_text = models.TextField()
    explan_text = models.TextField()
    def __unicode__(self):
        return self.answer_text
        
        
class Question(models.Model):
    """Multichoice question"""
    
    question_text = models.TextField()
    answers = models.ManyToManyField(Answer)
    correct_answer = models.ForeignKey(Answer, related_name="valid")
    
    def __unicode__(self):
        return self.question_text
    
        
class Quiz(models.Model):
    """A multi-choice quiz"""
    
    quiz_title = models.CharField(max_length=200)
    lesson = models.ForeignKey(Lesson)
    create_date = models.DateField(auto_now=True)
    author = models.ForeignKey(User)
    questions = models.ManyToManyField(Question)
    
    def __unicode__(self):
        return self.quiz_title

class Attempt(models.Model):
    """Responses made by user during an attempt of the quiz"""
    
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)
    taken_dt = models.DateTimeField(auto_now_add = True)
    question = models.ForeignKey(Question)
    answer_given = models.ForeignKey(Answer)
    score = models.IntegerField(default=0)
    
    #TODO intercept signal on attempt create/alter to calculate score

    def __unicode__(self):
        return "User: %s, Quiz: %s" % (self.user, self.quiz)
    