# urls for courses app
from django.conf.urls import include, patterns, url

urlpatterns = patterns('courses.views',
    url(r'^$', 'index', name='course_index'),
    url(r'^(?P<course_id>\d+)/edit/$', 'edit', name='course_edit'),
    url(r'^(?P<course_id>\d+)/enrol/$', 'enrol', name='course_enrol'),
    url(r'^(?P<course_id>\d+)/$', 'single', name='course_single'),
    url(r'^create/$', 'create', name='course_create'),
)

urlpatterns += patterns('',
    url(r'^(?P<course_id>\d+)/lesson/', include('lesson.urls')),
)

