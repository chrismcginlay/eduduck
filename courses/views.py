from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.shortcuts import (render_to_response, get_object_or_404, 
    get_list_or_404)
from django.template import RequestContext
from django.utils import timezone


from interaction.models import UserCourse, UserLesson
from .models import Course, Lesson

import pdb

import logging
logger = logging.getLogger(__name__)

#TODO: csrf check https://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
#^ esp. for AJAX, when time comes.

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
    """Prepare variables for detail of a single course
    
    There are 3 distinct pathways through this view as regards 'Progress' area:
    1. User is not authenticated. (Not logged in). Simplest case, present 
        'login to register' type message in course area.
    2. Authenticated, but not registered on this course. Provide 'register'.
    3. Authenticated and registered. Provide full context variables.
    """
  
    logger.info('Course id=' + str(course_id) + ' view')
    course = get_object_or_404(Course, pk=course_id)
    tz = request.user.bio.user_tz
    try:
        timezone.activate(tz)
    except:
        logger.error("Unknown timezone: %s. Drop to UTC", tz, exc_info=1)
        timezone.activate(timezone.utc)

    if request.user.is_authenticated():
        uc_set = request.user.usercourse_set.filter(course=course)
        if uc_set.exists():
            uc = uc_set[0]
            if request.method == 'POST':
                if 'course_withdraw' in request.POST:
                    if uc.active:
                        uc.withdraw()
                        logger.info(str(uc) + 'withdraws')
                    else:
                        logger.error("Can't withdraw course, reason: not active")                        
                if 'course_complete' in request.POST:
                    if uc.active:
                        uc.complete()
                        logger.info(str(uc) + 'completes')
                    else: 
                        logger.error("Can't complete course, reason: not active")
                if 'course_reopen' in request.POST:
                    if uc.withdrawn or uc.completed:
                        uc.reopen()
                        logger.info(str(uc) + 'reopens')
                    else:
                        logger.error("Can't reopen course, reason: already active")
            history = uc.hist2list()
            lessons_in_course = uc.course.lesson_set.all() #all lessons in course
            lessons_visited = uc.user.userlesson_set.all() #visited lessons

            #Prepare a list of tuples to pass to template. 
            #(lesson in course, userlesson interaction or None)
            lessons = []
            for lic in lessons_in_course:
                #see if the lesson has been visited
                try:
                    lv = lessons_visited.get(lesson=lic)
                except ObjectDoesNotExist:
                    lv = None   
                lessons.append((lic, lv))
            context_data = {'course': course,
                            'uc': uc,
                            'history': history,
                            'lessons': lessons,
                            'status': 'auth_reg'}    
        else:
            #Here we provide for case 2, user registers
            context_data = {'course': course,
                            'status': 'auth_noreg'}
            if request.method == 'POST':
                if 'course_register' in request.POST:
                    uc = UserCourse(user=request.user, course=course)
                    uc.save()
                    history = uc.hist2list()
                    context_data = {'course': course,
                                    'uc': uc,
                                    'history': history,
                                    'status': 'auth_reg'}
                    logger.info(str(uc) + 'registers')
                    
    else:
        context_data = {'course': course,
                        'status': 'anon'}
    logger.debug('courses.single request context: status='+context_data['status']) 
    template = 'courses/course_single.html'        
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance) 

   
def lesson(request, course_id, lesson_id):
    """Prepare variables for detail of individual lesson"""
    
    logger.info('Course id=' + str(course_id) + \
        ', Lesson id=' + str(lesson_id) + ' view')
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    tz = request.user.bio.user_tz
    try:
        timezone.activate(tz)
    except:
        logger.error("Unknown timezone: %s. Drop to UTC", tz, exc_info=1)
        timezone.activate(timezone.utc)
    
    #data on user interaction with lesson
    ul = None
    if request.user.is_authenticated():
        ul_set = request.user.userlesson_set.filter(lesson=lesson)
        if ul_set.exists():
            ul = ul_set[0]
            if request.method == 'POST':
                if 'lesson_complete' in request.POST:
                    if not ul.completed:
                        ul.complete()
                        logger.info(str(ul) + 'user completes')
                    else:
                        logger.error("Can't complete lesson, reason: already complete")
                if 'lesson_reopen' in request.POST:
                    if ul.completed:
                        ul.reopen()
                        logger.info(str(ul) + 'user reopens')
                    else:
                        logger.error("Can't re-open lesson, reason: not complete")
                history = ul.hist2list()
            else:
                #Not a form submission,
                #add distinct visit if more than 1 hour since last event
                history = ul.hist2list()
                last_event = history.pop()
                event_time = last_event[0]
                current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
                
                if (current_time - event_time) > timedelta(hours=1):
                    ul.visit() 
                history = ul.hist2list()                    
        else:
            #first visit. Must be registered on course
            try:
                request.user.usercourse_set.get(course=course)
                ul = UserLesson(user=request.user, lesson=lesson)
                ul.save()
                history = ul.hist2list()
            except:
                #not registered on course, do nothing quietly, no need to log
                history = None
    else:
        #User is not even authenticated, don't record anything
        ul = None
        history = None

    learning_intentions = lesson.learningintention_set.all()
    
    template = 'courses/course_lesson.html'
    context_data =  {'course':  course,
                     'lesson':  lesson,
                     'ul':      ul,
                     'history': history,
                     'learning_intentions': learning_intentions,
                    }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
     
    
