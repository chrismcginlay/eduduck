# Homepage views
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from registration.forms import RegistrationForm
from courses.models import Course

import logging; logger = logging.getLogger(__name__)

def home(request):
    """ Provide homepage (aka index.html) """ 
    
    logger.info("Homepage view")
    template = 'homepage/home.html'
    course_list = Course.objects.all()[:6]
    count_courses_used = len(course_list) # max. 6 sent to template
    courses_n_24ths = list()
    
    ## Group courses in 3s, divide widths into w 24ths proportional to 
    ## length of course name.
    for i in [3*j for j in range(1+(count_courses_used-1)/3)]:  # [0,3,6,..]
        c0,c1,c2 = (0,0,0)
        try:
            c0 = len(course_list[i+0].name)
            c1 = len(course_list[i+1].name)
            c2 = len(course_list[i+2].name)
        except IndexError:
            pass
        c_total = c0+c1+c2
        w0 = int(24*c0/c_total)
        w1 = int(24*c1/c_total)
        w2 = 24-w0-w1
        #Adjust w0,w1 to ensure total 24 if only 1 or 2 courses in row:
        if c1==0: (w0,w1,w2)=(24,0,0)
        if c2==0: (w1,w2)=(24-w0,0)
        try:
            courses_n_24ths.append((course_list[i+0], w0))
            courses_n_24ths.append((course_list[i+1], w1))
            courses_n_24ths.append((course_list[i+2], w2))
        except IndexError:
            pass
    register_form = RegistrationForm()
    context_data = {
        'register_form': register_form,
        'course_list': courses_n_24ths,
        'course_count': count_courses_used, 
    }

    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
