from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required

from quiz.models import Quiz, Question, Answer, Attempt
from quiz.forms import QuestionForm, AnswerForm, QuizForm, QuizTakeForm
from quiz.forms import QuestionAttemptForm, make_question_attempt_form
from quiz.forms import quiz_forms

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
#def quiz_take(request, quiz_id):
#    """An attempt by a user to take a quiz"""
#
#    quiz = get_object_or_404(Quiz, pk=quiz_id)
#    question_list = quiz.questions.all()
#    
#    #list_answer_lists is a list of lists of possible answers,
#    #one list per question
#    list_answer_lists = list()
#    for question in question_list:
#        #list_answer_lists.append([(a.id, a.answer_text) for a in question.answers.all()])
#        list_answer_lists.append(question.answers.all())
#    QuestionFormSet = formset_factory(QuestionAttemptForm)
#    QuestionFormSet.form = staticmethod(curry(QuestionAttemptForm, choices=list_answer_lists ))
#
#    if request.method == 'POST':
#        formset = QuestionFormSet(request.POST, instance=quiz)
#        if formset.is_valid():
#            #process cleaned data, save
#            return redirect(quizzes)
#            
#    else:
#        formset = QuestionFormSet()
#        
#    template = 'quiz/quiz_take.html'
#    context_data = {    'formset': formset,
#                        'quiz': quiz,
#                    }
#                    
#    return render_to_response(template, context_data, RequestContext(request))
    
    
@login_required
def testquestion(request):
    #For development purposes, hardcoding the following
    q = Quiz.objects.get(pk = 1)     #capital cities quiz
    u = request.user
    question = Question.objects.get(pk=1)   #The sweden question
    partial_attempt_data = Attempt(user=u, quiz=q, question=question)
    answerlist = [(a.id, a.answer_text) for a in question.answers.all()]
    if request.method == 'POST':
        #Method A
        form = QuestionAttemptForm(request.POST, choices=answerlist, instance=partial_attempt_data)
        
        #Method B
        #form_cls = make_question_attempt_form(question)
        #form = form_cls(request.POST)
        
        if form.is_valid():
            answer_given = form.cleaned_data['answer_given']
            form.save(commit=False)
            if question.correct_answer == answer_given:
                form.score = 1
            else:
                form.score = 0
            form.save()
            feedback_data = {   'score': form.score,
                                 'question': question,
                                 'answer_given': answer_given,
                            }
            return render_to_response('quiz/question_feedback.html', feedback_data)
            
    else:
        #Method A
        form = QuestionAttemptForm(choices=answerlist, instance=partial_attempt_data)

        #Method B        
        #form = make_question_attempt_form(question)
                
    context_data = {'form':form, 'question':question, 'answerlist':answerlist}    
    return render_to_response('quiz/single_question.html', context_data, RequestContext(request))


# The following paradigm works fine for a single question.
# Not so amenable to multiquestion quiz. Initially I had thought to re-use 
# this to generate an entire quiz.
def question_pose(request, q_id, quiz_id):
    """Pose a single question"""
    question = Question.objects.get(pk=q_id)
    u = request.user
    quiz = Quiz.objects.get(pk=quiz_id)
    partial_attempt_data = Attempt(user=u, quiz=quiz, question=question)
    answerlist = [(a.id, a.answer_text) for a in question.answers.all()]
    if request.method == 'POST':
        form = QuestionAttemptForm(request.POST, 
                                   choices=answerlist, 
                                   instance=partial_attempt_data)
        if form.is_valid():
            answer_given = form.cleaned_data['answer_given']
            form.save(commit=False)
            if question.correct_answer == answer_given:
                form.score = 1
            else:
                form.score = 0
            form.save()
            feedback_data = {'score': form.score,
                             'question': question,
                             'answer_given': answer_given,
                            }
            return render_to_response('quiz/question_feedback.html', 
                                      feedback_data)
            
    else:
        form = QuestionAttemptForm(choices=answerlist, 
                                   instance=partial_attempt_data)
                
    context_data = {'form':form, 
                    'question':question, 
                    'answerlist':answerlist}    
    return render_to_response('quiz/single_question.html', 
                              context_data, 
                              RequestContext(request))


#another attempt to get this figured out
@login_required
def quiz_take2(request, quiz_id):
    """An attempt by a user to take a quiz"""

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question_set = quiz.questions.all()
    question_list = [q.question_text for q in question_set]
    
    if request.method == 'POST':
        form_list = quiz_forms(quiz, question_list, request.POST)
        zip_list = zip(form_list, question_list)
        
        #Validity Check, score and save
        valid_count = 0    
        total_score = 0
        for zitem in zip_list:
            f = zitem[0]
            q = zitem[1]
            if f.is_valid():
                valid_count+= 1
                f.calculate_score
                total_score += f.score
                
        feedback_data = {    'zip_list': zip_list, #debug
                             'quiz': quiz,
                             'valid_count': valid_count,
                             'total_score': total_score,
                             'form_list': form_list,  #debug 
                        }                
        return render_to_response('quiz/quiz_feedback.html',
                                  feedback_data,
                                  RequestContext(request))
        
    else:
        form_list = quiz_forms(quiz, question_list)
        zip_list = zip(form_list, question_list)
    
    return render_to_response('quiz/quiz_take2.html', 
                              {'quiz':quiz, 
                               'form_list':form_list,
                               'zip_list': zip_list,
                               'question_list': question_list,
                               }, 
                                RequestContext(request))