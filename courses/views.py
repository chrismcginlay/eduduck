#courses/views.py

from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.exceptions import (
    ObjectDoesNotExist,
    PermissionDenied,
    ValidationError,
)
from django.forms.models import inlineformset_factory
from django.shortcuts import (
    redirect,
    render,
    render_to_response, 
    get_object_or_404, 
    get_list_or_404,
)

from django.template import RequestContext
from django.utils import timezone
from django.utils.html import escape

from interaction.models import UserCourse, UserLesson
from lesson.forms import LessonEditForm
from lesson.models import Lesson
from video.forms import VideoForm
from video.models import Video
from .forms import CourseFullForm
from .models import Course

import logging
logger = logging.getLogger(__name__)

LessonInlineFormset = inlineformset_factory(
    Course, Lesson, form=LessonEditForm, extra=3)
VideoInlineFormset = inlineformset_factory(
    Course, Video, form=VideoForm, extra=1, exclude=('lesson',))

def _courses_n_24ths(clist):
    """ Take a list of courses cl, 3 courses at a time. Set their widths to 
    fit names neatly on a row. Return a list of tuples (course, width) """
    
    count_courses_used = len(clist)
    if count_courses_used==0: return None
    courses_n_24ths = list()
    for i in [3*j for j in range(1+(count_courses_used-1)/3)]:  # [0,3,6,..]
        c0,c1,c2 = (0,0,0)
        try:
            c0 = len(clist[i+0].name)
            c1 = len(clist[i+1].name)
            c2 = len(clist[i+2].name)
        except IndexError:
            pass
        c_total = c0+c1+c2
        w0 = int(24*c0/c_total)
        w1 = int(24*c1/c_total)
        w2 = 24-w0-w1

        #Adjust w0,w1 to ensure total 24 if only 1 or 2 courses in row:
        if c1==0: (w0,w1,w2)=(24,0,0)
        if c2==0: (w1,w2)=(24-w0,0)
        try:
            courses_n_24ths.append((clist[i+0], w0))
            courses_n_24ths.append((clist[i+1], w1))
            courses_n_24ths.append((clist[i+2], w2))
        except IndexError:
            pass
    return courses_n_24ths

def _user_permitted_to_edit_course(user, course_id):
    
    course = get_object_or_404(Course, pk=course_id)
    if not user.is_authenticated(): return False
    if not (user.id ==  course.organiser_id or user.id == course.instructor_id):
        return False
    return True

@login_required
def edit(request, course_id):
    """View to allow instructor/organiser to edit course"""
    
    if _user_permitted_to_edit_course(request.user, course_id):
        course = get_object_or_404(Course, pk=course_id)
        if request.method=='POST':
            course_form = CourseFullForm(
                request.POST, prefix='course_form', instance=course)
            lesson_formset = LessonInlineFormset(
                request.POST, prefix='lesson_formset', instance=course)
            video_formset = VideoInlineFormset(
                request.POST, prefix='video_formset', instance=course)
            if course_form.is_valid():
                course_form.save()
                logger.info("Course (id={0}) edited".format(course.pk))
            if lesson_formset.is_valid():
                lesson_formset.save()
                logger.info("Lessons for course id {0} edited".format(course.pk))
            if video_formset.is_valid():
                video_formset.save()
                logger.info("Video for course id {0} saved".format(course.pk))
            if (course_form.is_valid() 
                and lesson_formset.is_valid()
                and video_formset.is_valid()):
                logger.info("course (id={0}) edited".format(course.pk))
                return redirect(course)
            else:
                t = 'courses/course_edit.html'
                c = { 'course_form': course_form,
                      'lesson_formset': lesson_formset,
                      'video_formset': video_formset, 
                      'course': course,
                }
                return render(request, t, c)
        else:
            course_form = CourseFullForm(
                prefix='course_form', instance=course)
            lesson_formset = LessonInlineFormset(
                prefix='lesson_formset', instance=course)
            video_formset = VideoInlineFormset(
                prefix='video_formset', instance=course)
            t = 'courses/course_edit.html'
            c = { 'course_form': course_form,
                  'lesson_formset': lesson_formset,
                  'video_formset': video_formset, 
                  'course': course,
            }
            return render(request, t, c)
    else:
        logger.info("Unauthorized attempt to edit course {0}".format(course_id))
        raise PermissionDenied
    
@login_required
def create(request):
    """View to allow logged in users to create a course"""
    
    if request.method=='POST':
        course_form = CourseFullForm(request.POST)
        if course_form.is_valid():
            code = course_form.cleaned_data['code']
            name = course_form.cleaned_data['name']
            abstract = course_form.cleaned_data['abstract']
            organiser_id = request.user.id
            instructor_id = request.user.id
            course = Course.objects.create(
                code = code,
                name = name,
                abstract = abstract,
                organiser_id = organiser_id,
                instructor_id = instructor_id,
            )
            logger.info("New course (id={0}) created".format(course.pk))
            return redirect(course)
    else:
        name_desired = escape(request.GET.get('course_short_name', '')) # dict get
        data = {'name': name_desired}
        course_form = CourseFullForm(initial=data)
    t = 'courses/course_create.html'
    return render(request, t, {'form': course_form})

def index(request):
    """Prepare variables for list of all courses"""

    logger.info('Course index view')
    course_list = Course.objects.all()
    course_count = Course.objects.count
    template = 'courses/course_index.html'
    cn24ths = _courses_n_24ths(course_list)
    context_data = { 'course_list':  cn24ths,
                     'course_count': course_count,
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
            context_data = { 'course': course,
                             'uc': uc,
                             'history': history,
                             'lessons': lessons,
                             'status': 'auth_reg'}    
        else:
            #Here we provide for case 2, user registers
            context_data = { 'course': course,
                             'status': 'auth_noreg'}
            if request.method == 'POST':
                if 'course_register' in request.POST:
                    uc = UserCourse(user=request.user, course=course)
                    uc.save()
                    history = uc.hist2list()
                    context_data = { 'course': course,
                                     'uc': uc,
                                     'history': history,
                                     'status': 'auth_reg'}
                    logger.info(str(uc) + 'registers')
                    
    else:
        context_data = { 'course': course,
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
    
    #Add a flag if the current user is the organiser or instructor for the 
    #course, so template can display edit button
    if request.user.is_authenticated():
        if request.user.pk == course.organiser_id  \
                or request.user.pk == course.instructor_id:
            context_data.update({'user_can_edit': True})
        else:
            context_data.update({'user_can_edit': False})

    logger.debug('courses.single request context: status='+context_data['status']) 
    template = 'courses/course_single.html'        
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance) 

