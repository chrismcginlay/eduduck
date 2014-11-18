from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import (render, get_object_or_404, get_list_or_404)
    
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from courses.models import Course
from .forms import ProfileEditForm

import logging
logger = logging.getLogger(__name__)

@login_required
def profile(request):
    """Display the user's profile details"""
    
    logger.info('Profile id=' + str(request.user.id) + ' view')
    template = 'profile/profile.html'
    profile = request.user.profile
    assert(profile)

    usercourses = request.user.usercourse_set.all()
    ruid = request.user.id
    taughtcourses = Course.objects.filter(
        Q(organiser__id=ruid) | Q(instructor__id=ruid))

    context_data = {
        'profile': profile, 
        'usercourses': usercourses,
        'taughtcourses': taughtcourses,
    }
    # Add further context if required:    
    if request.user.is_authenticated():
        try:
            auth_via = request.session['social_auth_last_login_backend']
        except KeyError:
            auth_via = request.session['_auth_user_backend']
            assert(auth_via==u'django.contrib.auth.backends.ModelBackend')
            auth_via = "username and password. Oooh, how old fashioned."
        finally:
            context_data.update({'auth_via': auth_via})
 
    return render(request, template, context_data)

@login_required
def edit(request):
    """Allow edit of user's profile details"""
    
    logger.info('Profie id=' + str(request.user.id) + ' edit')    
    template = 'profile/profile_edit.html'
    profile = request.user.profile
    assert(profile)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            profile.user_tz = form.cleaned_data['user_tz']
            profile.accepted_terms = form.cleaned_data['accepted_terms']
            profile.signature_line = form.cleaned_data['signature_line']
            profile.description = form.cleaned_data['description']
            profile.webpage = form.cleaned_data['webpage']
            profile.save()
            return HttpResponseRedirect('/accounts/profile/')
    else:
        form = ProfileEditForm(instance=profile)
        
    context_data = {    'profile': profile,
                        'form': form, }
    return render(request, template, context_data)


def public(request, user_id):
    """Display publicly visible profile data"""

    logger.info('Profile id=' + str(user_id) + ' public profile view')
    template = 'profile/profile_public.html'
    user = get_object_or_404(User, pk=user_id)
    
    #pass only the required public user data, prevent extraction from context data
    fullname = user.get_full_name()
    motto = user.profile.signature_line
    timezone = user.profile.user_tz
    webpage = user.profile.webpage
    description = user.profile.description
    
    context_data = { 
        'fullname': fullname,
        'motto': motto,
        'timezone': timezone,
        'webpage': webpage,
        'description': description,
    }
    return render(request, template, context_data)
