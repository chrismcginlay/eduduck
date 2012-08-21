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
          
#Refer: http://stackoverflow.com/questions/622982/django-passing-custom-form-parameters-to-formset
def make_question_attempt_form(question, *args, **kwargs):
    class QuestionAttemptForm2(forms.Form):
        """Generate form for a single question using 'closure'"""
        answer_given = forms.ModelChoiceField(
            queryset=Answer.objects.filter(question=question),
            widget = forms.RadioSelect
        )
    
        class Meta:
            widgets = {
                'answer_given': forms.RadioSelect()
            }
        
    #Note requirement to prefix each question form with 
    #unique question id
    return QuestionAttemptForm2(prefix=str(question.id))

        
class QuizTakeForm(forms.ModelForm):
    class Meta:
        model = Attempt
        exclude = {'user','quiz'}
    QuestionFormSet = formset_factory(QuestionAttemptForm, extra=2)


def quiz_forms(quiz, question_list):
    questions = Question.objects.filter(quiz=quiz)
    form_list = []
    for idx, question in enumerate(questions):
        form_list.append(make_question_attempt_form(question))
    return form_list