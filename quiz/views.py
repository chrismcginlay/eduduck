from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required

from quiz.models import Quiz, Question, Answer
from quiz.forms import QuestionForm, AnswerForm, QuizForm, QuizTakeForm, QuestionTakeForm

#TODO Use generic views?

#http://www.peachybits.com/2011/09/django-1-3-form-api-modelform-example/

######################################
# Questions
######################################
def questions(request):
    """View all questions"""
    question_list = Question.objects.all()
    
    template = 'quiz/questions.html'
    context_data = { 'question_list': question_list,}
    context_instance = RequestContext(request)
    
    return render_to_response(template, context_data, context_instance)
    
    
def question_add(request):
    """Add question using model form"""
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(questions)
    else:
        form = QuestionForm()
        
    template = 'quiz/question_add.html'
    context_data = { 'form_add': form, }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    

def question_edit(request, question_id):
    """Add question using model form"""
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect(questions)
    else:
        form = QuestionForm(instance=question)
        
    template = 'quiz/question_edit.html'
    context_data = {'form_edit':        form,
                    'question_id':      question_id,
                    }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    
#TODO implement confirmation prior to deletion
def question_delete(request, question_id):
    """Delete a question"""
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
    
    return redirect(question)
    
###################################
# Answers
###################################
def answers(request):
    """View all answers"""
    answer_list = Answer.objects.all()
    
    template = 'quiz/answers.html'
    context_data = { 'answer_list': answer_list,}
    context_instance = RequestContext(request)
    
    return render_to_response(template, context_data, context_instance)
    
    
def answer_add(request):
    """Add answer using model form"""
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(answers)
    else:
        form = AnswerForm()
        
    template = 'quiz/answer_add.html'
    context_data = { 'form_add': form, }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    

def answer_edit(request, answer_id):
    """Add answer using model form"""
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect(answers)
    else:
        form = AnswerForm(instance=answer)
        
    template = 'quiz/answer_edit.html'
    context_data = {'form_edit':        form,
                    'answer_id':      answer_id,
                    }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    
#TODO implement confirmation prior to deletion
def answer_delete(request, answer_id):
    """Delete a answer"""
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()
    
    return redirect(answers)

############################################
# Quiz
############################################
def quizzes(request):
    """View all quizzes"""
    quiz_list = Quiz.objects.all()
    
    template = 'quiz/quizzes.html'
    context_data = { 'quiz_list': quiz_list,}
    context_instance = RequestContext(request)
    
    return render_to_response(template, context_data, context_instance)
    
    
def quiz_add(request):
    """Add quiz using model form"""
    
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(quizzes)
    else:
        form = QuizForm()
        
    template = 'quiz/quiz_add.html'
    context_data = { 'form_add': form, }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    

def quiz_edit(request, quiz_id):
    """Add quiz using model form"""
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect(quizzes)
    else:
        form = QuizForm(instance=quiz)
        
    template = 'quiz/quiz_edit.html'
    context_data = {'form_edit':    form,
                    'quiz_id':      quiz_id,
                    }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    
#TODO implement confirmation prior to deletion
def quiz_delete(request, quiz_id):
    """Delete a quiz"""
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    quiz.delete()
    
    return redirect(quizzes)

    
###########################
#see p170
#@login_required
def quiz_take(request, quiz_id):
    """An attempt by a user to take a quiz"""

    #Following builds a dictionary with questions and answers.
    q = get_object_or_404(Quiz, pk=quiz_id)
    qanda_data = dict()
    for question in q.questions.all():
        qanda_data[question] = (question.answers.all(), question.correct_answer)
            
    if request.method == 'POST':
        form = QuizTakeForm(request.POST, instance=quiz_take)
        if form.is_valid():
            #process data in form.cleaned_data
            #form.save()
            return HttpResponseRedirect('some kind of result page')
    else:
        form = QuizTakeForm()
            
    template = 'quiz/quiz_take.html'
    context_data = {    'form_take': form,
                        'quiz': q,
                        'qanda': qanda_data,
                    }
    context_instance = RequestContext(request)
    
    return render_to_response(template, context_data, context_instance)
    
from django.forms.formsets import formset_factory
def testquestion(request):
    """See if I can get a single question up"""
    
    question = Question.objects.get(pk=1)
    if request.method == 'POST':
        form = QuestionTakeForm(request.POST)
        if form.is_valid():
            return redirect(Question)
    else:
        data = {'answer':question.answers.all()}
        form = QuestionTakeForm(initial=data)
        QuestionFormSet = formset_factory(QuestionTakeForm, extra=2)
        formset = QuestionFormSet()
      
    context_data = { 'form': form, 'fs': formset, 'q':question.question_text}
    return render_to_response('quiz/testquestion.html',context_data,RequestContext(request))
    