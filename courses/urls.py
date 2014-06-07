# urls for courses app
from django.conf.urls import patterns, url
from .views import index, single

urlpatterns = patterns('courses.views', 
    url(r'^$', 'index', name='course_index'),
    url(r'^(?P<course_id>\d+)/$', 'single', name='course_single'),
    url(r'^create/$', 'create', name='course_create'),
)

urlpatterns += patterns('',
    url(r'^(?P<course_id>\d+)/lesson/(?P<lesson_id>\d+)/$',
        'lesson.views.lesson', name='course_lesson'),
)