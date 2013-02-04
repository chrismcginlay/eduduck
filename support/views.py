from django.core.mail import send_mail

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import SupportForm

def support(request):
    """Provide a support/contact email form"""
    
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
        
    context_instance = RequestContext(request)
    return render_to_response('support/support.html', {'support_form': form}, context_instance)