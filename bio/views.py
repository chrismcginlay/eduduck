from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import (render_to_response, get_object_or_404, 
    get_list_or_404)
    
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import BioEditForm

import pdb

@login_required
def bio(request):
    template = 'bio/bio.html'
    bio = request.user.get_profile()
    assert(bio)
#    user_lessons = profile.userprofile_lesson_set.all()
    context_data = {    'bio': bio, }
#                        'user_lessons': user_lessons,}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)

@login_required
def bio_edit(request):
    template = 'bio/bio_edit.html'
    bio = request.user.get_profile()
    assert(bio)
    pdb.set_trace()
    if request.method == 'POST':
        form = BioEditForm(request.POST)
        if form.is_valid():
            bio2 = form.save(commit=False)
            bio2.user = User.objects.get(pk=request.user.id)
            bio2.save()
            return HttpResponseRedirect('/accounts/bio/')
    else:
        form = BioEditForm(instance=bio)
        
    context_data = {    'bio': bio,
                        'form': form, }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)