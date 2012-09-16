from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy
from courses.models import Lesson
from django.shortcuts import get_list_or_404
import datetime

# TODO eventually create other types of quiz, using an abstract base class
# DONE: get everything working with simple multichoice.
class Answer(models.Model):
    """Multichoice style answer. 
    
    Represent a possible answer along with explanatory text
    
    Attributes:
        answer_text     Human readable text of possible answer
        explan_text     Explanation of why this answer is right/wrong
    
    """
    
    answer_text = models.TextField("possible answer")
    explan_text = models.TextField(
                    "answer advice", 
                    help_text="Advice on how relevant this answer is")
    
    def __unicode__(self):
        return self.answer_text
        
#TODO Question needs a sequence number (i.e. sequence in quiz)        
# Would be used to order and label questions
# Should be unique to a quiz and question numbers should be contiguous
# within each quiz.
class Question(models.Model):
    """Multichoice question.
    
    Attributes:
        question_text   Human readable text of the question
        answers         m-mField - all contender answers
        correct_answer  ForeignKey - the 'correct' answer
        
    """
    
#TODO ensure that answers includes correct_answer, possibly could do this
#when the question is included in a quiz
    question_text = models.TextField(help_text="The question as presented "
        "to the user")
    #TODO change the following field to 1-2-many
    answers = models.ManyToManyField(Answer, verbose_name="possible answers")    
    correct_answer = models.ForeignKey(Answer, related_name="valid")
    
    def __unicode__(self):
        return self.question_text

        
class Quiz(models.Model):
    """A multi-choice quiz.
    
    Attributes:
        quiz_title  Human readable name of the quiz
        lesson      ForeignKey - lesson to which quiz belongs
        create_date Date on which quiz was first created
        author      ForeignKey - author user
        questions   m-mField - all questions constituting this course
    
    """
    quiz_title = models.CharField(max_length=200)
    lesson = models.ForeignKey(Lesson)
    create_date = models.DateField("date quiz created", auto_now=True)
    author = models.ForeignKey(User)
    questions = models.ManyToManyField(Question)
    
    class Meta:
        verbose_name = ugettext_lazy('quiz')
        verbose_name_plural = ugettext_lazy('quizzes')
        
    def __unicode__(self):
        return self.quiz_title


class QuizAttempt(models.Model):
    """Record each time a user attempts a particular quiz
    
    Individual question responses are stored in QuestionAttempt
    
    Attributes:
        user            ForeignKey - who is attempting the quiz
        quiz            ForeignKey - the quiz
        taken_dt        Date of this quiz attempt
    """
    quiz = models.ForeignKey(Quiz)
    user = models.ForeignKey(User)
    taken_dt = models.DateTimeField("date of quiz attempt")

    def save(self, *args, **kwargs):
        """Set timestamp on save"""
        if not self.id:
            self.taken_dt = datetime.datetime.now()
        super(QuizAttempt, self).save(*args, **kwargs)

    def quiz_score(self):
        """Calculate total score of all questions in the attempt"""
        question_attempt_set = get_list_or_404(QuestionAttempt, 
                                               quiz_attempt = self.pk)
        score = 0
        for question_attempt in question_attempt_set:
            score += question_attempt.score
        return score
    
    def __unicode__(self):
        return "User: %s, Quiz: %s, Score: %s" % (self.user, 
                                                  self.quiz, 
                                                  self.quiz_score)
        
        
class QuestionAttempt(models.Model):
    """Responses made by user during an attempt of the quiz.attname
    
    Note that we DO need to record the question object here too, since we 
    will record the user's response to each question in the database, and we
    will score each response separately.
    
    Attributes:
        question        ForeignKey - a question of the quiz
        answer_given    The answer object the user thinks to be 'correct'
        score           Points allocated to answer_given
    
    """
    quiz_attempt = models.ForeignKey(QuizAttempt)
    question = models.ForeignKey(Question)
    answer_given = models.ForeignKey(Answer, verbose_name="user's answer")
    score = models.IntegerField(default=0)

        
    def __unicode__(self):
        return "Quiz Attempt: %s, Question: %s, Score: %s" % (
        self.quiz_attempt, self.question, self.score)
    