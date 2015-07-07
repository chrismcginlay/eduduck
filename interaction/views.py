#interaction/views.py

import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpResponse, 
    HttpResponseForbidden,
    HttpResponseRedirect
)
from django.shortcuts import (
    render, 
    get_object_or_404
)
from django.utils import timezone    
from django.views.decorators.csrf import ensure_csrf_cookie

from outcome.models import LearningIntentionDetail
from attachment.models import Attachment
from .models import (
    UserCourse, 
    UserLesson,
    UserLearningIntention,
    UserLearningIntentionDetail,
    UserAttachment
)

import logging
logger = logging.getLogger(__name__)

@login_required
def usercourse_single(request, user_id, course_id):
    """Decode and display user's history for a single course"""
    
    logger.info("User:"+str(user_id)+",Course:"+str(course_id)+" view interactions")
    uc = get_object_or_404(UserCourse, course=course_id, user=user_id)
    history = uc.hist2list()
    try:
        tz = request.user.profile.user_tz    
        timezone.activate(tz)
    except:
        logger.warning("Reverting to default timezone (UTC)")
        timezone.activate(timezone.utc)
        
    template = 'interaction/usercourse_single.html'
    context = {'uc': uc, 'history': history}
    return render(request, template, context)

@login_required
def userlesson_single(request, user_id, lesson_id):
    """Display user interactions with single lesson"""
    
    logger.info("User:"+str(user_id)+",Lesson:"+str(lesson_id)+" view interactions")
    ul = get_object_or_404(UserLesson, lesson=lesson_id, user=user_id)
    history = ul.hist2list()
    try:
        tz = request.user.profile.user_tz    
        timezone.activate(tz)
    except:
        logger.warning("Reverting to default timezone (UTC)")
        timezone.activate(timezone.utc)
    
    template = 'interaction/userlesson_single.html'
    context = {'ul': ul, 'history': history}
    return render(request, template, context)

# TODO: possibly redundant view
@login_required
def ajax_learningintentiondetail_status(request, lid_id):
    if request.is_ajax():
        conditions = ['red', 'amber', 'green']
        try:
            ulid = UserLearningIntentionDetail.objects.get(
                user__id=request.user.id, learning_intention_detail__id=lid_id)
            status = ulid.get_status()
        except ObjectDoesNotExist:
            status = 'red'

        result = {'status':status,}
        jresult = json.dumps(result)
        return HttpResponse(jresult, content_type="application/json")
    else:
        return HttpResponseForbidden()
    
@login_required
def userlearningintentiondetail_single(request, user_id, lid_id):
    """Probably pointlessly display user interaction with single LID"""
    
    #TODO: nothing actually links to this view?
    #Hmm. Might in the future. Leaving in for now at MVP0.2
    ulid = get_object_or_404(UserLearningIntentionDetail, 
                             user=user_id, 
                             learning_intention_detail=lid_id)
    logger.info(ulid.__unicode__()+" view interactions")
    history = ulid.hist2list()
    try:
        tz = request.user.profile.user_tz    
        timezone.activate(tz)
    except:
        logger.warning("Reverting to default timezone (UTC)")
        timezone.activate(timezone.utc)
    
    template = 'interaction/userlearningintentiondetail_single.html'
    context = {'ulid': ulid, 'history': history}
    return render(request, template, context)

@ensure_csrf_cookie
def userlearningintentiondetail_cycle(request, lid_id):
    """For AJAX use in cycling learning intention details (LID)"""
  
    if request.user.is_authenticated():
        lid = LearningIntentionDetail.objects.get(pk=lid_id)
        course = lid.learning_intention.lesson.course
      
        # If user not enrolled, redirect to enrol on course homepage 
        try:
             UserCourse.objects.get(user=request.user.id, course=course)
        except ObjectDoesNotExist:
            jsonr = json.dumps({
                'authenticated':True,
                'enrolled':False,
                'course_pk':course.pk,
            })
            return HttpResponse(jsonr, content_type='application/json')

        #Need to ensure the interaction object exists for user, LID

        ulid_set = UserLearningIntentionDetail.objects.get_or_create( 
                            user=request.user, 
                            learning_intention_detail=lid)
        ulid = ulid_set[0]

        #Need now to ensure that an interaction object exists for user, LI
        uli_set = UserLearningIntention.objects.get_or_create(
            user = request.user,
            learning_intention = lid.learning_intention)
        uli = uli_set[0]
        logger.info("Cycling learning intention detail ULID: "+str(ulid))
        ulid.cycle()

        #Update progress for the entire Learning Intention
        #uli.progress() is combined SC and LO progress
        result = {
            'enrolled': True,
            'authenticated': True,
            'condition':ulid.condition,
            'progress':uli.progress()
        }
        jresult = json.dumps(result)
        return HttpResponse(jresult, content_type='application/json')

    else: #not authenticated
        jsonr = json.dumps({'authenticated': False, 'enrolled':False})
        return HttpResponse(jsonr, content_type='application/json')
    
@login_required
def userlearningintention_progress_bar(request, lid_id):
    """Return tuple for jQuery to create a progress bar
    
    Could this be made more generic? Moved to a utilities area as it is more
    generally applicable than merely to learning intentions.
    """

    li = (LearningIntentionDetail.objects.get(pk=lid_id)).learning_intention
    uli = get_object_or_404(UserLearningIntention,
                            user = request.user,
                            learning_intention = li)    
    logger.info('User:'+str(request.user.pk)+\
        'progress update LI id:'+str(li.pk))
    result = {'progress': uli.progress()}
    jresult = json.dumps(result)
    return HttpResponse(jresult, content_type='application/json')

@login_required
def attachment_download(request, att_id):
    """Record interaction with download prior to handing off to webserver
    
    Basic idea is to hook in to downloads here to update record of downloads
    then trigger webserver download with File field of underlying model.
    """

    #Some implementation notes:
    #3 use cases:
    #   1. User not logged in. Forbidden. 
    #   2. User logged in but not enrolled on course. Redirect to enrol page 
    #   3. User logged in and enrollled. Download, log it.

    attachment = get_object_or_404(Attachment, id=att_id)    
    try:
        course_record = request.user.usercourse_set.get(course=attachment.course)
    except AttributeError:
        course_record = None
    except ObjectDoesNotExist:
        try:
            course_record = request.user.usercourse_set.get(course=attachment.lesson.course)
        except (AttributeError, ObjectDoesNotExist) as err:
            course_record = None
    if course_record:
        #get_or_create return tuple (object, success_state)
        uad = UserAttachment.objects.get_or_create(user=request.user, attachment=attachment)
        #newly created record will automatically record download
        if (uad[1]==False): uad[0].record_download()
        redir_link = uad[0].attachment.get_absolute_url()               
    else:
        try:
            parent_course_id = attachment.course.id
        except AttributeError:
            parent_course_id = attachment.lesson.course.id
        redir_link = '/courses/{0}/enrol/'.format(parent_course_id)
    logger.debug('Absolute download URI for redirect is ' + redir_link)	
    return HttpResponseRedirect(redir_link)

