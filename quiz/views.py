from quiz.models import Quiz
from courses.models import Lesson, Course
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

def quiz_central(request, course_id):
    """All quizes within a particular course"""
    
    u = request.user
    c = get_object_or_404(Course, pk=course_id)
    
    qs = c.lesson_set.all()
    template = 'quiz/quiz_central.html'
    context_data = {    'user': u,
                        'course': c,
                        'quizset': qs,
                    }
    context_instance = RequestContext(request)
    
    return render_to_response(template, context_data, context_instance)
    