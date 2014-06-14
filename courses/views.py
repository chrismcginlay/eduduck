#courses/views.py

from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import (
    redirect,
    render_to_response, 
    get_object_or_404, 
    get_list_or_404,
)

from django.template import RequestContext
from django.utils import timezone

from registration.forms import RegistrationForm

from interaction.models import UserCourse, UserLesson
from lesson.models import Lesson
from .forms import CourseFullForm
from .models import Course

import logging
logger = logging.getLogger(__name__)

def create(request):
    """View to allow users to create a course"""

    if request.method=='POST':
        course_form = CourseFullForm(request.POST)
        try:
            course = Course.objects.create(
                code = request.POST['code'],
                name=request.POST['name'],
                abstract=request.POST['abstract'],
                organiser_id=request.user.pk,
                instructor_id=request.user.pk,
                level='1',
                credits=1,
            )
            course.full_clean()
            course.save()
            logger.info("Course created {0}".format(course.pk))
            return redirect(course)
        except ValidationError:
            logger.info("User failed to create course")
        
    else:
        logger.info("Course create view")
        t = 'courses/course_create.html'
        cd = {'form': CourseFullForm()}
        ci = RequestContext(request)
        return render_to_response(t, cd, ci)
    
def index(request):
    """Prepare variables for list of all courses"""

    logger.info('Course index view')
    course_list = Course.objects.all()
    course_count = Course.objects.count
    register_form = RegistrationForm()
    template = 'courses/course_index.html'

    context_data = {'course_list':  course_list,
                    'course_count': course_count,
                    'register_form': register_form,
                   }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)

def iterNone(): 
    """Make None type iterable for zip function used below"""

    yield None

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
                        
    #get attachment data ready
    userattachments_attachments_tuple = [] #to be tuples (user_att|None, uri)
    attachments = course.attachment_set.all()
    user_att_in_course = []

    #TODO try to merge these two loops together,
    #merge the entire attachment construction with above request.user loop
    if request.user.is_authenticated():
        #Now get only the user_attachments relevant to the lesson at hand
        user_attachments = request.user.userattachment_set.all()
        for ua in user_attachments:
            if ua.attachment in attachments:
                user_att_in_course.append(ua)

        for attachment in attachments:
            try:
                ua = user_attachments.get(attachment=attachment)
            except ObjectDoesNotExist:
                ua = None
            userattachments_attachments_tuple.append((ua, attachment))
    else:
        userattachments_attachments_tuple = zip(iterNone(), attachments)
    context_data.update({'attachments': userattachments_attachments_tuple})
    
    logger.debug('courses.single request context: status='+context_data['status']) 
    template = 'courses/course_single.html'        
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance) 

