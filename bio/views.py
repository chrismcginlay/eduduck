from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import (render_to_response, get_object_or_404, 
    get_list_or_404)
    
from django.contrib.auth.decorators import login_required

from .forms import BioEditForm

import logging
logger = logging.getLogger(__name__)

@login_required
def bio(request):
    """Display the user's bio details"""
    
    logger.info('Bio id=' + str(request.user.id) + ' view')
    template = 'bio/bio.html'
    bio = request.user.get_profile()
    assert(bio)
#    user_lessons = profile.userprofile_lesson_set.all()
    context_data = {    'bio': bio, }
#                        'user_lessons': user_lessons,}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)

@login_required
def edit(request):
    """Allow edit of user's bio details"""
    
    logger.info('Bio id=' + str(request.user.id) + ' edit')    
    template = 'bio/bio_edit.html'
    bio = request.user.get_profile()
    assert(bio)
    if request.method == 'POST':
        form = BioEditForm(request.POST, instance=bio)
        if form.is_valid():
            bio.accepted_terms = form.cleaned_data['accepted_terms']
            bio.signature_line = form.cleaned_data['signature_line']
            bio.description = form.cleaned_data['description']
            bio.webpage = form.cleaned_data['webpage']
            bio.save()
            return HttpResponseRedirect('/accounts/bio/')
    else:
        form = BioEditForm(instance=bio)
        
    context_data = {    'bio': bio,
                        'form': form, }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)