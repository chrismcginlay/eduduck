from django import forms
from quiz.models import Quiz, Question, Answer, Attempt
    
#http://www.peachybits.com/2011/09/django-1-3-form-api-modelform-example/
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz

          
