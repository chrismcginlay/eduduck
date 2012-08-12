from django import forms
from django.forms.formsets import formset_factory
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

class QuestionTakeForm(forms.Form):
    #question = forms.CharField()
    answer = forms.CharField()
    
class QuizTakeForm(forms.ModelForm):
    class Meta:
        model = Attempt
        exclude = {'user','quiz'}
    QuestionFormSet = formset_factory(QuestionTakeForm, extra=2)
