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

class QuestionAttemptForm(forms.ModelForm):
    """Generate form for a single question"""
    class Meta:
        model = Attempt
        exclude = ('user', 'quiz', 'question', 'score')
        widgets = {
            'answer_given': forms.RadioSelect()
        }
        
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', None)
        super(QuestionAttemptForm, self).__init__(*args, **kwargs)
        if choices is not None:
            self.fields['answer_given'].choices = choices
          
    
class QuizTakeForm(forms.ModelForm):
    class Meta:
        model = Attempt
        exclude = {'user','quiz'}
    QuestionFormSet = formset_factory(QuestionAttemptForm, extra=2)
