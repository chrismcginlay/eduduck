from django.shortcuts import (
    get_object_or_404,
    get_list_or_404,
    redirect, 
    render,
)
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from quiz.models import Quiz, Question, Answer, QuizAttempt, QuestionAttempt
from quiz.forms import QuestionForm, AnswerForm, QuizForm

from django.http import HttpResponseRedirect
#TODO Use generic views?

#http://www.peachybits.com/2011/09/django-1-3-form-api-modelform-example/

######################################
# Questions
######################################
def questions(request):
    """View all questions"""
    question_list = get_list_or_404(Question)
    
    template = 'quiz/questions.html'
    context_data = { 'question_list': question_list,}
    return render(request, template, context_data)
    
    
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
    assert form
    return render(request, template, context_data)
    

def question_edit(request, question_id):
    """Add question using model form"""
    assert question_id
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
    assert form
    return render(request, template, context_data)
    
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
    answer_list = get_list_or_404(Answer)
    
    template = 'quiz/answers.html'
    context_data = { 'answer_list': answer_list,}
    return render(request, template, context_data)
    
    
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
    assert form
    return render(request, template, context_data)
    

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
    assert form
    return render(request, template, context_data)
    
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
    quiz_list = get_list_or_404(Quiz)
    
    template = 'quiz/quizzes.html'
    context_data = { 'quiz_list': quiz_list,}
    
    return render(request, template, context_data)
    
    
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
    assert form
    return render(request, template, context_data)
    

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
    assert form
    return render(request, template, context_data)
    
#TODO implement confirmation prior to deletion
def quiz_delete(request, quiz_id):
    """Delete a quiz"""
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    quiz.delete()
    
    return redirect(quizzes)

@login_required
def quiz_take(request, quiz_id):
    """An attempt by a user to complete a quiz"""
    
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.method == "POST": #form is submitted
        try:
            #Create a dictionary of submitted answers for each question,
            #question => answer given by user
            selected_answer = dict()
            for question in quiz.questions.all():
                qstring = "Q" + str(question.id)
                selected_answer[qstring] = question.answers.get(pk=request.POST[qstring])
        except (KeyError, Answer.DoesNotExist):
            #Redisplay quiz form
            return render(
                request,
                'quiz/quiz_take.html',
                {'quiz': quiz,
                 'error_message': "Please answer all of the questions.",},
            )
        #form is submitted and complete, process it
        #save the quiz attempt, display results.
        quiz_attempt = QuizAttempt(user = request.user, quiz = quiz)
        quiz_attempt.save()
        for question in quiz.questions.all():
            qstring = "Q" + str(question.id)
            answer_given = Answer.objects.get(pk=int(request.POST[qstring]))
            if answer_given == question.correct_answer:
                score = 1
            else:
                score = 0
            attempt = QuestionAttempt(quiz_attempt = quiz_attempt,
                                      question= question, 
                                      answer_given = answer_given, 
                                      score = score) 
            attempt.save()
        return HttpResponseRedirect(reverse('quiz.views.quiz_results', args=(quiz_id,)))

    else: #unbound
        return render(
            request,
            'quiz/quiz_take.html',
            {'quiz': quiz,},
        )
            
def quiz_results(request, quiz_id):
    """Show the results of the quiz attempt"""
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    try:
        quiz_attempts = QuizAttempt.objects.filter(quiz=quiz, 
                                      user=request.user).order_by('-taken_dt')
    except:
        raise Http404
    #Create a list of all the attempts at a quiz by a user
    #each element of the list is a list of question responses
#    attempt_digest = list()
#    for qa in quiz_attempts:
#        question_attempts = QuestionAttempt.objects.filter(quiz_attempt=qa)
#        attempt_digest.append(question_attempts)
        
    return render(
        request, 
        'quiz/quiz_results.html',
        {'quiz_attempts': quiz_attempts,},
    )

