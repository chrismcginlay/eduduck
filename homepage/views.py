# Homepage views
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from courses.forms import CourseNameForm
from courses.models import Course
from courses.views import _courses_n_24ths

import logging; logger = logging.getLogger(__name__)

def home(request):
    """ Provide homepage (aka index.html) """ 
    
    logger.info("Homepage view")
    template = 'homepage/home.html'
    course_list = Course.objects.all()[:6]
    courses_n_24ths = _courses_n_24ths(course_list)
    course_form = CourseNameForm()
    context_data = {
        'course_form': course_form,
        'course_list': courses_n_24ths,
    }

    if request.user.is_authenticated():
        try:
            auth_via = request.session['social_auth_last_login_backend']
        except KeyError:
            auth_via = request.session['_auth_user_backend']
            assert(auth_via==u'django.contrib.auth.backends.ModelBackend')
            auth_via = "username and password. Oooh, how old fashioned."
        finally:
            context_data.update({'auth_via': auth_via})
 
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)

