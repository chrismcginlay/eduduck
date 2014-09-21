# Views for lesson app
from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import timezone

from interaction.models import UserLesson
from .models import Lesson


import logging; logger = logging.getLogger(__name__)



def iterNone(): 
    """Make None type iterable for zip function used below"""
    
    yield None
    
def _user_permitted_to_edit_lesson(user, lesson_id):
    
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if not user.is_authenticated(): return False
    if not (user.id ==  lesson.course.organiser_id 
        or user.id == lesson.course.instructor_id):
        return False
    return True

def lesson(request, course_id, lesson_id):
    """Prepare variables for detail of individual lesson"""

    logger.info('Course id=' + str(course_id) + \
        ', Lesson id=' + str(lesson_id) + ' view')
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course

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
            except ObjectDoesNotExist:
                #not registered on course, do nothing quietly, no need to log
                history = None
    else:
        #User is not even authenticated, don't record anything
        ul = None
        history = None

    learning_intentions = lesson.learningintention_set.all()
    
    #get attachment data ready
    userattachments_attachments_tuple = [] #to be tuples (user_att|None, uri)
    attachments = lesson.attachment_set.all()
    user_att_in_lesson = []

    #TODO try to merge these two loops or similar 
    if request.user.is_authenticated():
        #Now get only the user_attachments relevant to the lesson at hand
        user_attachments = request.user.userattachment_set.all()
        for ua in user_attachments:
            if ua.attachment in attachments:
                user_att_in_lesson.append(ua)

        for attachment in attachments:
            try:
                ua = user_attachments.get(attachment=attachment)
            except ObjectDoesNotExist:
                ua = None
            userattachments_attachments_tuple.append((ua, attachment))
    else:
        userattachments_attachments_tuple = zip(iterNone(), attachments)
    
    template = 'lesson/lesson_single.html'
    context_data =  {'course':  course,
                     'lesson':  lesson,
                     'ul':      ul,
                     'history': history,
                     'attachments': userattachments_attachments_tuple,
                     'learning_intentions': learning_intentions,
                    }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
     
