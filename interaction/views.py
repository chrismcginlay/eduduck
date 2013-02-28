import logging
import datetime
import json

import pdb

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import (render_to_response, get_object_or_404, 
    get_list_or_404)
    
from django.contrib.auth.decorators import login_required

from .models import UCActions, UserCourse

logger = logging.getLogger(__name__)

@login_required
def usercourse_single(request, user_id, course_id):
    """Decode and display user's history for a single course"""
    
    logger.info("Showing single course interaction for user")
    uc = get_object_or_404(UserCourse, course=course_id, user=user_id)
    history = json.loads(uc.history)
    reconstructed_history = []
    pdb.set_trace()
    for row in history:
        date = datetime.datetime.fromtimestamp(row[0])
        action = UCActions[row[1]]
        reconstructed_history.append((date, action))
        
    template = 'interaction/usercourse_single.html'
    context_data = {'uc': uc, 'history': reconstructed_history}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)

