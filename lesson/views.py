# Views for lesson app
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import (
    ObjectDoesNotExist,
    PermissionDenied,
)
from django.forms.models import inlineformset_factory, modelform_factory
from django.shortcuts import (
    redirect,
    render, 
    get_object_or_404, 
)
from django.template import RequestContext
from django.utils import timezone

from attachment.forms import AttachmentForm
from attachment.models import Attachment
from interaction.models import UserLesson
from outcome.forms import LearningIntentionForm
from outcome.models import LearningIntention
from video.forms import VideoForm
from video.models import Video
from .forms import LessonEditForm
from .models import Lesson


import logging; logger = logging.getLogger(__name__)

VideoInlineFormset = inlineformset_factory(
    Lesson, Video, form=VideoForm, extra=1, exclude=('course',))
AttachmentInlineFormset = inlineformset_factory(
    Lesson, Attachment, form=AttachmentForm, extra=1, exclude=('course',))
LearningIntentionInlineFormset = inlineformset_factory(
    Lesson, 
    LearningIntention, 
    form=LearningIntentionForm, 
    extra=5, 
    exclude=('course',)
)

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

def _user_can_view_lesson(user, lesson):
    course = lesson.course
    first_lesson = course.lesson_set.first()
    if lesson==first_lesson:
        return True
    return False 

def visit(request, course_id, lesson_id): 
    """Prepare variables for detail of individual lesson"""

    logger.info('Course id=' + str(course_id) + \
        ', Lesson id=' + str(lesson_id) + ' view')
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course

    if not _user_can_view_lesson(request.user, lesson):
        return redirect(course)
    
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
            #first visit. Must be enrolled on course
            try:
                request.user.usercourse_set.get(course=course)
                ul = UserLesson(user=request.user, lesson=lesson)
                ul.save()
                history = ul.hist2list()
            except ObjectDoesNotExist:
                #not enrolled on course, do nothing quietly, no need to log
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
    context_data =  {
        'course':  course,
        'lesson':  lesson,
        'ul':      ul,
        'history': history,
        'attachments': userattachments_attachments_tuple,
        'learning_intentions': learning_intentions,
    }
    if _user_permitted_to_edit_lesson(request.user, lesson_id):
        context_data.update({'user_can_edit_lesson': True})
    else:
        context_data.update({'user_can_edit_lesson': False})

    return render(request, template, context_data)

@login_required
def edit(request, lesson_id, course_id):
    if not(_user_permitted_to_edit_lesson(request.user, lesson_id)):
        logger.info("Unauthorized attempt to edit lesson {0}".format(lesson_id))
        raise PermissionDenied()
    else:        
        LessonFormNoCourse = modelform_factory(
            Lesson, 
            form=LessonEditForm,
            exclude=('course',)
        )
        lesson = get_object_or_404(Lesson, id=lesson_id)
        if request.method=='POST':
            lesson_form = LessonFormNoCourse(
                request.POST, prefix='lesson_form', instance=lesson)
            video_formset = VideoInlineFormset(
                request.POST, prefix='video_formset', instance=lesson)
            attachment_formset = AttachmentInlineFormset(
                request.POST, 
                request.FILES, 
                prefix='attachment_formset', 
                instance=lesson
            )
            learning_intention_formset = LearningIntentionInlineFormset(
                request.POST,
                prefix='learning_intention_formset',
                instance=lesson
            ) 
            if lesson_form.is_valid():
                lesson_form.save()
                logger.info("Lesson (id={0}) edited".format(lesson.pk))
            if video_formset.is_valid():
                video_formset.save()
                logger.info("Video for lesson id {0} saved".format(lesson.pk))
            if attachment_formset.is_valid():
                attachment_formset.save()
                logger.info("Attachment for lesson id {0} saved".format(lesson.pk))
            if learning_intention_formset.is_valid():
                learning_intention_formset.save()
            if (lesson_form.is_valid() 
                and video_formset.is_valid()
                and attachment_formset.is_valid()
                and learning_intention_formset.is_valid()):
                logger.info("Lesson (id={0}) edited".format(lesson.pk))
                return redirect(lesson)
            else:
                t = 'lesson/lesson_edit.html'
                c = {
                    'lesson': lesson,
                    'course': lesson.course,
                    'lesson_form': lesson_form,
                    'video_formset': video_formset,
                    'attachment_formset': attachment_formset,
                    'learning_intention_formset': learning_intention_formset,
                }
                return render(request, t, c)
        else: #not post
            lesson_form = LessonFormNoCourse(
                prefix='lesson_form', instance=lesson)
            video_formset = VideoInlineFormset(
                prefix='video_formset', instance=lesson)
            attachment_formset = AttachmentInlineFormset(
                prefix='attachment_formset', instance=lesson)
            learning_intention_formset = LearningIntentionInlineFormset(
                prefix='learning_intention_formset', instance=lesson)
            t = 'lesson/lesson_edit.html'
            c = { 
                'lesson': lesson,
                'lesson_form': lesson_form,
                'video_formset': video_formset, 
                'attachment_formset': attachment_formset,
                'learning_intention_formset': learning_intention_formset,
                'course': lesson.course,
            }
            return render(request, t, c)
 
