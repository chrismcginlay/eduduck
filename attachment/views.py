#attachments/views.py
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .models import Attachment

def view_metadata(request):
    """A view to render such things as description, size etc"""

    return 
    
def download(request, att_id, att_code):
    """Demonstrate detection of download prior to handing off to webserver
    
    Basic idea is hook in here to update counters or record of downloads
    then trigger webserver download with File field of underlying model.
    TODO move this functionality into the interaction module
    """
    
    attachment = get_object_or_404(Attachment, id=att_id)
    return HttpResponseRedirect(attachment.attachment.url)