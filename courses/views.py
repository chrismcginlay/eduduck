from courses.models import Course, Lesson, UserProfile_Lesson
from django.http import HttpResponseRedirect
from django.shortcuts import (render_to_response, get_object_or_404, 
    get_list_or_404)
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

#TODO: csrf check https://docs.djangoproject.com/en/dev/ref/contrib/csrf/
#TODO: improve request context:
#http://lincolnloop.com/blog/2008/may/10/getting-requestcontext-your-templates/

def index(request):
    """List of all courses"""
    course_list = Course.objects.all()
    course_count = Course.objects.count
    template = 'courses/index.html'
    context_data = {'course_list':   course_list,
                    'course_count':  course_count,
                   }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    

def single(request, course_id):
    """Detail of a single course"""
    
    course = get_object_or_404(Course, pk=course_id)
    template = 'courses/single.html'
    context_data = {'course': course}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    
    
@login_required
def lesson(request, course_id, lesson_id):
    """Detail of individual lesson"""
    
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    #data on user interaction with lesson
    user_lessons = lesson.userprofile_lesson_set.all()
    
    template = 'courses/lesson.html'
    context_data =  {'course':  course,
                     'lesson':  lesson,
                     'user_lessons':     user_lessons,
                    }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
    
@login_required
def user_profile(request):
    template = 'registration/user_profile.html'
    profile = request.user.get_profile()
    user_lessons = profile.userprofile_lesson_set.all()
    context_data = {    'profile': profile,
                        'user_lessons': user_lessons,}
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)


def created(request):
    """Confirmation that user was created"""
    
    return render_to_response('registration/registration_complete.html')
    
    
#http://www.djangobook.com/en/beta/chapter12/
def register(request):
    """Register new user"""
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            u = form.cleaned_data['username']
            userprof = "/users/" + u + "/"
            #TODO this should use reverse()
            return HttpResponseRedirect(userprof)
    else:
        form = UserCreationForm()
    
    template = 'registration/registration_form.html'
    context_data = { 'form': form}
    context_instance = RequestContext(request)
    assert form
    return render_to_response(template, context_data, context_instance)