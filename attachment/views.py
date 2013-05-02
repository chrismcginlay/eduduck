#attachment/views.py
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from .models import Attachment

import logging
logger = logging.getLogger(__name__)

def metadata(request, att_id):
    """A view to render such things as description, size etc"""
    
    att = get_object_or_404(Attachment, pk=att_id)
    logger.info("User ID:%s, attachment ID:%s; accessing metadata")
    template = 'attachment/attachment_metadata.html'
    context_data = {'attachment':  att}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
