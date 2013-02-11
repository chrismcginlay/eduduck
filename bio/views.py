from django.template import RequestContext
from django.shortcuts import (render_to_response, get_object_or_404, 
    get_list_or_404)
    
from django.contrib.auth.decorators import login_required

@login_required
def bio(request):
    template = 'registration/user_profile.html'
    profile = request.user.get_profile()
    user_lessons = profile.userprofile_lesson_set.all()
    context_data = {    'profile': profile,
                        'user_lessons': user_lessons,}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
