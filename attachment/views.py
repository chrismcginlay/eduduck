#attachment/views.py
from django.shortcuts import get_object_or_404, render

from .models import Attachment

import logging
logger = logging.getLogger(__name__)

def metadata(request, att_id):
    """A view to render such things as description, size etc"""
    
    att = get_object_or_404(Attachment, pk=att_id)
    logger.info("User ID:%s, attachment ID:%s; accessing metadata")
    template = 'attachment/attachment_metadata.html'
    context = {'att':  att}
    return render(request, template, context)
