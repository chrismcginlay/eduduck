from django.core.mail import send_mail

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext

from .forms import SupportForm

import logging
logger = logging.getLogger(__name__)

def support(request):
    """Provide a support/contact email form"""
    
    logger.info('Support view')
    if request.method=="POST":
        form = SupportForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            send_mail(cdata['subject'],
                      cdata['message'],
                      cdata.get('email', 'support@eduduck.com'),
                        ['support@eduduck.com'],
            )
            return HttpResponseRedirect('/support/thanks/')
    else:
        form = SupportForm()
        
    return render(
        request, 
        'support/support.html',
        {'support_form': form}, 
    )
