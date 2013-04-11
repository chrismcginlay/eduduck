import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import (render_to_response, 
                              get_object_or_404)
    
from django.contrib.auth.decorators import login_required

from outcome.models import LearningIntention, LearningIntentionDetail
from .models import UserCourse, UserLesson, UserLearningIntentionDetail

import pdb

import logging
logger = logging.getLogger(__name__)

@login_required
def usercourse_single(request, user_id, course_id):
    """Decode and display user's history for a single course"""
    
    logger.info("User:"+str(user_id)+",Course:"+str(course_id)+" view interactions")
    uc = get_object_or_404(UserCourse, course=course_id, user=user_id)
    history = uc.hist2list()
        
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
    
    template = 'interaction/userlesson_single.html'
    context_data = {'ul': ul, 'history': history}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    
@login_required
def userlearningintentiondetail_single(request, user_id, lid_id):
    """Probably pointlessly display user interaction with single LID"""
    
    #TODO: nothing actually links to this view?
    ulid = get_object_or_404(UserLearningIntentionDetail, 
                             user=user_id, 
                             learning_intention_detail=lid_id)
    logger.info(ulid.__unicode__()+" view interactions")
    history = ulid.hist2list()
    
    template = 'interaction/userlearningintentiondetail_single.html'
    context_data = {'ulid': ulid, 'history': history}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)

@login_required
def userlearningintentiondetail_cycle(request, lid_id):
    """For AJAX use in cycling learning intention details (LID)"""
    
    lid = LearningIntentionDetail.objects.get(pk=lid_id)
    ulid_set = UserLearningIntentionDetail.objects.get_or_create( 
                        user=request.user, 
                        learning_intention_detail=lid)
    ulid = ulid_set[0]
    logger.info("Cycling learning intention detail ULID: "+str(ulid))
    ulid.cycle()
    result = {'condition':ulid.condition}
    jresult = json.dumps(result)
    return HttpResponse(jresult, mimetype='application/json')
    
@login_required
def userlearningintention_progressbar(request, learning_intention_id):
    """For AJAX use, update progress bars after LID cycle"""
    
    li_id = get_object_or_404(LearningIntention, pk=lid_id)
    try:
        ulid_set = UserLearningIntentionDetail.objects.get( 
                        user=request.user, 
                        learning_intention_detail=lid)
    except DoesNotExist:
        pass
                        