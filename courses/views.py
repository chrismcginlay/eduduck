#courses/views.py
from datetime import datetime, timedelta
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import (
    ObjectDoesNotExist,
    PermissionDenied,
    ValidationError,
)
from django.forms.models import inlineformset_factory
from django.shortcuts import (
    redirect,
    render,
    get_object_or_404, 
    get_list_or_404,
)

from django.template import RequestContext
from django.utils import timezone
from django.utils.html import escape

from attachment.models import Attachment
from attachment.forms import AttachmentForm
from checkout.models import Payment, PricedItem
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
AttachmentInlineFormset = inlineformset_factory(
    Course, Attachment, form=AttachmentForm, extra=1, exclude=('lesson',))

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

def _user_permitted_to_publish_course(user, course_id):
    return _user_permitted_to_edit_course(user, course_id)

@login_required
def publish(request, course_id):
    if _user_permitted_to_publish_course(request.user, course_id):
        course = get_object_or_404(Course, pk=course_id)
        context = {
            'course': course,
        }
        if course.published:
            context.update({
                'course_already_published': True,
            })
        if request.method=='POST':
            if 'cancel_publish' in request.POST:
                context.update({
                    'publish_cancelled': True,
                })
            if 'course_publish' in request.POST:
                course.published = True
                course.save()
        context.update({
            'course_published': course.published,
        })
        template = 'courses/course_publish.html'
        return render(request, template, context) 
    else:
        logger.info("Unauthorized attempt to edit course {0}".format(course_id))
        raise PermissionDenied

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
            attachment_formset = AttachmentInlineFormset(
                request.POST, 
                request.FILES,
                prefix='attachment_formset',
                instance=course
            )
            if course_form.is_valid():
                course_form.save()
                logger.info("Course (id={0}) edited".format(course.pk))
            if lesson_formset.is_valid():
                lesson_formset.save()
                logger.info("Lessons for course id {0} edited".format(course.pk))
            if video_formset.is_valid():
                video_formset.save()
                logger.info("Video for course id {0} saved".format(course.pk))
            if attachment_formset.is_valid():
                attachment_formset.save()
                logger.info("Attachment for course id {0} saved".format(course.pk))
            if (course_form.is_valid() 
                and lesson_formset.is_valid()
                and video_formset.is_valid()
                and attachment_formset.is_valid()):
                logger.info("course (id={0}) edited".format(course.pk))
                return redirect(course)
            else:
                t = 'courses/course_edit.html'
                c = { 'course_form': course_form,
                      'lesson_formset': lesson_formset,
                      'video_formset': video_formset, 
                      'attachment_formset': attachment_formset,
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
            attachment_formset = AttachmentInlineFormset(
                prefix='attachment_formset', instance = course)
            t = 'courses/course_edit.html'
            c = { 'course_form': course_form,
                  'lesson_formset': lesson_formset,
                  'video_formset': video_formset, 
                  'attachment_formset': attachment_formset,
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
    c = { 'form': course_form }
    return render(request, t, c)

@login_required
def enrol(request,course_id):
    """View to encourage enrolment.

    Suggest user enrols when non-enrolled user tries to access certain 
    resources. Course instructor or organiser gets error message"""
    
    course = get_object_or_404(Course, pk=course_id)
    course_type = ContentType.objects.get_for_model(Course)
    priced_item = get_object_or_404(
        PricedItem, content_type_id=course_type.id, object_id=course_id)
    fee_value = priced_item.fee_value
    if request.user.is_authenticated():
        status='auth_notenrolled'
        if request.user.usercourse_set.filter(course=course).exists():
            status='auth_enrolled'
        if (request.user == course.organiser or 
                request.user == course.instructor):
            status='auth_bar_enrol'         
    else:
        status='anon'

    t = 'courses/course_enrol.html'
    c = {
        'course': course, 
        'status': status,
        'fee_value': fee_value,
    }
    return render(request, t, c) 

def index(request):
    """Prepare variables for list of all courses"""

    logger.info('Course index view')
    course_list = Course.objects.filter(published=True) | Course.objects.filter(organiser=request.user.id) | Course.objects.filter(instructor=request.user.id)
    course_count = course_list.count()
    template = 'courses/course_index.html'
    cn24ths = _courses_n_24ths(course_list)
    c = {
        'course_list':  cn24ths,
        'course_count': course_count, 
    }
    return render(request, template, c)

def iterNone(): 
    """Make None type iterable for zip function used below"""

    yield None

def detail(request, course_id):
    """View for detail of a single course"""
   
    logger.debug('Course id=' + str(course_id) + ' view')
    course = get_object_or_404(Course, pk=course_id)
    course_type = ContentType.objects.get_for_model(Course)
    priced_item = get_object_or_404(
        PricedItem, content_type_id=course_type.id, object_id=course_id)
    fee_value = priced_item.fee_value
    user_can_edit = False
    history = None
    lessons = None
    attachments = None

    context = {
        'course':course,
        'fee_value':fee_value,
        'fee_value_cents':fee_value*100,
        'currency':priced_item.currency,
    }

    if request.user.is_authenticated():
        try:
            uc = request.user.usercourse_set.get(course__id = course_id)
            status = 'auth_enrolled'
        except ObjectDoesNotExist:
            uc = None
            if (request.user == course.organiser or 
                    request.user == course.instructor):
                status = 'auth_bar_enrol'
                user_can_edit = True
            else:
                status = 'auth_not_enrolled'
    else:
        uc = None
        status = 'noauth'
            
    if request.method == 'POST':
        if 'stripeToken' in request.POST and status == 'auth_not_enrolled':
            stripe.api_key = settings.STRIPE_SECRET_KEY 
            token = request.POST['stripeToken']
            try:
                charge = stripe.Charge.create(
                    amount=int(fee_value*100), # amount in cents, again
                    currency=priced_item.currency,
                    source=token,
                    description="Example charge"
                )
                current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
                #Now record payment
                payment = Payment(
                    content_object=course,
                    paying_user=request.user,
                    fee_value=fee_value,
                    currency=priced_item.currency,
                    datestamp=current_time
                )
                payment.save()
                #Enrol the student
                uc = UserCourse(user=request.user, course=course)
                uc.save()
                status = 'auth_enrolled'
                logger.info(str(uc) + 'enrols')
            except stripe.error.CardError, e:
                pass

        if 'course_enrol' in request.POST:
            course_type = ContentType.objects.get_for_model(course)
            if not(fee_value == 0):
                payment = Payment.objects.get(
                    content_type__pk=course_type.id, object_id=course.id, paying_user=request.user)
            uc = UserCourse(user=request.user, course=course)
            uc.save()
            status = 'auth_enrolled'
            logger.info(str(uc) + 'enrols')
            
        if 'course_complete' in request.POST and status == 'auth_enrolled':
            if uc.active:
                uc.complete()
                logger.info(str(uc) + 'completes')
            else: 
                logger.error("Can't complete course, reason: not active")
        if 'course_withdraw' in request.POST and status == 'auth_enrolled':
            if uc.active:
                uc.withdraw()
                logger.info(str(uc) + 'withdraws')
            else:
                logger.error("Can't withdraw, reason: not active")
        if 'course_reopen' in request.POST and status == 'auth_enrolled':
            if not uc.active:
                uc.reopen()
                logger.info(str(uc) + 'reopens')
            else:
                logger.error("Can't reopen, reason: already active")

    if uc:
        history = uc.hist2list()

        user_lessons = uc.user.userlesson_set.filter(
            lesson__course__pk=course_id)
        lessons_in_course = uc.course.lesson_set.all() #all lessons in course
        #lessonv - lesson visited
        lessons = [(
            alesson, next((lessonv for lessonv in 
                uc.user.userlesson_set.filter(lesson__pk=alesson.pk)), None)
        ) for alesson in lessons_in_course]

        user_attachments = uc.user.userattachment_set.filter(
            attachment__course__pk=course_id)
        attachments_in_course = uc.course.attachment_set.all()
        #attd - attachments downloaded
        attachments = [(
            next((attd for attd in uc.user.userattachment_set.filter(attachment__pk=anattachment.pk)), None), anattachment) for anattachment in attachments_in_course]

    else: #no uc
        attachments = [(None, att) for att in course.attachment_set.all()]

    context.update({
        'attachments': attachments,
        'history': history,
        'lessons': lessons,
        'status': status,
        'user_can_edit': user_can_edit,
        'uc': uc,
    })
    template = 'courses/course_detail.html'
    return render(request, template, context) 

