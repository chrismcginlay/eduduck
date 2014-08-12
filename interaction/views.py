#interaction/views.py

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import (render_to_response, 
                              get_object_or_404)
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone    
from django.contrib.auth.decorators import login_required

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
        tz = request.user.bio.user_tz    
        timezone.activate(tz)
    except:
        logger.warning("Reverting to default timezone (UTC)")
        timezone.activate(timezone.utc)
        
    template = 'interaction/usercourse_single.html'
    context_data = {'uc': uc, 'history': history}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)

@login_required
def userlesson_single(request, user_id, lesson_id):
    """Display user interactions with single lesson"""
    
    logger.info("User:"+str(user_id)+",Lesson:"+str(lesson_id)+" view interactions")
    ul = get_object_or_404(UserLesson, lesson=lesson_id, user=user_id)
    history = ul.hist2list()
    try:
        tz = request.user.bio.user_tz    
        timezone.activate(tz)
    except:
        logger.warning("Reverting to default timezone (UTC)")
        timezone.activate(timezone.utc)
    
    template = 'interaction/userlesson_single.html'
    context_data = {'ul': ul, 'history': history}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    
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
        tz = request.user.bio.user_tz    
        timezone.activate(tz)
    except:
        logger.warning("Reverting to default timezone (UTC)")
        timezone.activate(timezone.utc)
    
    template = 'interaction/userlearningintentiondetail_single.html'
    context_data = {'ulid': ulid, 'history': history}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)

@login_required
def userlearningintentiondetail_cycle(request, lid_id):
    """For AJAX use in cycling learning intention details (LID)"""
    
    lid = LearningIntentionDetail.objects.get(pk=lid_id)
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
    result = {'condition':ulid.condition, 'progress':uli.progress()}
    jresult = json.dumps(result)
    return HttpResponse(jresult, mimetype='application/json')
    
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
    return HttpResponse(jresult, mimetype='application/json')

@login_required
def attachment_download(request, att_id):
    """Record interaction with download prior to handing off to webserver
    
    Basic idea is to hook in to downloads here to update record of downloads
    then trigger webserver download with File field of underlying model.
    """

    #Some implementation notes:
    #If using login_required decorator the request.user.usercourse_set ORM call
    #will work or throw ObjectDoesNotExist
    #If not using login_required decorator (ie anon user can download) then 
    #request.user.usercourse_set will throw AttributeError due to AnonymousUser
    #not having a usercourse_set attribute.
    #So catch it. Just NB that if using login_required, then the exception will
    #never be thrown.
    attachment = get_object_or_404(Attachment, id=att_id)    
    try:
        course_record = request.user.usercourse_set.get(course=attachment.course)
    except AttributeError:
        course_record = None
    except ObjectDoesNotExist:
        try:
            course_record = request.user.usercourse_set.get(course=attachment.lesson.course)
        except ObjectDoesNotExist:
            course_record = None
    if course_record:
        #get_or_create return tuple (object, success_state)
        uad = UserAttachment.objects.get_or_create(user=request.user, attachment=attachment)
        #newly created record will automatically record download
        if (uad[1]==False): uad[0].record_download()
        dl_link = uad[0].attachment.get_absolute_url()               
    else:
        dl_link = attachment.get_absolute_url()
    logger.debug('Absolute download URI for redirect is ' + dl_link)	
    redir_resp = HttpResponseRedirect(dl_link)
    return redir_resp


