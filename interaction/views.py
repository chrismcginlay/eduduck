import logger
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import (render_to_response, get_object_or_404, 
    get_list_or_404)
    
from django.contrib.auth.decorators import login_required

from .models import UserCourse

@login_required
def usercourse(request, course_id, user_id):
    """Decode and display user's history for a single course"""
    
    logger.info("Showing single course interaction for user")
    uc = get_object_or_404(UserCourse, course=course_id, user=user_id)
    template = 'interaction/usercourse_single.html'
    context_data = {'uc': uc}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)

