from django.shortcuts import (render_to_response, get_object_or_404, 
    get_list_or_404)
from django.template import RequestContext

from courses.models import Course, Lesson, LearningIntention

import logging

logger = logging.getLogger(__name__)

#TODO: csrf check https://docs.djangoproject.com/en/dev/ref/contrib/csrf/
#TODO: improve request context:
#http://lincolnloop.com/blog/2008/may/10/getting-requestcontext-your-templates/

def index(request):
    """Prepare variables for list of all courses"""
    
    logger.info('Course index view')
    course_list = Course.objects.all()
    course_count = Course.objects.count
    if request.user.is_authenticated():
        profile = request.user.get_profile()
    else:
        profile = None
    template = 'courses/course_index.html'
    context_data = {'course_list':  course_list,
                    'course_count': course_count,
                    'profile':      profile,
                   }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    
    
def single(request, course_id):
    """Prepare variables for detail of a single course"""
    
    course = get_object_or_404(Course, pk=course_id)
    template = 'courses/course_single.html'
    context_data = {'course': course}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    
    
def lesson(request, course_id, lesson_id):
    """Prepare variables for detail of individual lesson"""

    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    #data on user interaction with lesson
    user_lessons = lesson.userprofile_lesson_set.all()
    learning_intentions = lesson.learningintention_set.all()
    
    template = 'courses/course_lesson.html'
    context_data =  {'course':  course,
                     'lesson':  lesson,
                     'user_lessons':        user_lessons,
                     'learning_intentions': learning_intentions,
                    }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    

def learning_intention(request, lesson_id, learning_intention_id):
    """Prepare variables for learning intention template"""
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    learning_intention = get_object_or_404(LearningIntention, 
                                           id=learning_intention_id) 
    
    template = 'courses/course_lint.html'
    context_data =  {
                    'lesson':  lesson,
                    'learning_intention': learning_intention,
                    }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    
    
