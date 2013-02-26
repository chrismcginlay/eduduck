from json import JSONDecoder
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import (render_to_response, get_object_or_404, 
    get_list_or_404)
    
from django.contrib.auth.decorators import login_required

from .models import UserCourse

import logging
logger = logging.getLogger(__name__)

@login_required
def usercourse_single(request, user_id, course_id):
    """Decode and display user's history for a single course"""
    
    logger.info("Showing single course interaction for user")
    uc = get_object_or_404(UserCourse, course=course_id, user=user_id)
    history = JSONDecoder(uc.history)
    template = 'interaction/usercourse_single.html'
    context_data = {'uc': uc, 'history': history}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)

