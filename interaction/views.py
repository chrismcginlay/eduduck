from django.conf import settings
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import (render_to_response, get_object_or_404, 
    get_list_or_404)
    
from django.contrib.auth.decorators import login_required

from .models import UserCourse, UserLesson, UserSuccessCriterion

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
def usersuccesscriterion_single(request, user_id, sc_id):
    """Probably pointlessly display user interaction with single SC"""
    
    #TODO: nothing actually links to this view?
    usc = get_object_or_404(UserSuccessCriterion, 
                            user=user_id, 
                            success_criterion=sc_id)
    logger.info(usc.__unicode__()+" view interactions")
    history = usc.hist2list()
    
    template = 'interaction/usersuccesscriterion_single.html'
    context_data = {'usc': usc, 'history': history}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    