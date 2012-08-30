from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

#TODO decouple quiz app URLs from courses - see p38

urlpatterns = patterns('django.views.generic.simple',
    (r'^$',    'direct_to_template', {'template': 'home.html'}),
    (r'^about/$', 'direct_to_template', {'template': 'about.html'}),
)

urlpatterns += patterns('courses.views',
    url(r'^courses/$', 'index'),
    url(r'^courses/(?P<course_id>\d+)/$', 'single'),
    url(r'^courses/(?P<course_id>\d+)/lesson/(?P<lesson_id>\d+)/$',
        'lesson'),
    url(r'^users/$', 'user_profile'),
)
    #TODO consider deletion of item below
#   url(r'^courses/(?P<course_id>\d+)/quizzes/$', 'quiz.views.quizzes'),    
    
    #temporary question handler
urlpatterns += patterns('quiz.views',
    url(r'^questions/$', 'questions'),
    url(r'^question_add/$', 'question_add'),    
    url(r'^question_edit/(?P<question_id>\d+)/$', 'question_edit'),
    url(r'^question_delete/(?P<question_id>\d+)/$', 'question_delete'),

    #temporary answer handler
    url(r'^answers/$', 'answers'),
    url(r'^answer_add/$', 'answer_add'),    
    url(r'^answer_edit/(?P<answer_id>\d+)/$', 'answer_edit'),
    url(r'^answer_delete/(?P<answer_id>\d+)/$', 'answer_delete'),

    #temporary quiz handler
    url(r'^quizzes/$', 'quizzes'),
    url(r'^quiz_add/$', 'quiz_add'),    
    url(r'^quiz_edit/(?P<quiz_id>\d+)/$', 'quiz_edit'),
    url(r'^quiz_delete/(?P<quiz_id>\d+)/$', 'quiz_delete'),
    url(r'^quiz_take/(?P<quiz_id>\d+)/$', 'quiz_take2'),

    #testing only
    url(r'^questiontest/$', 'testquestion'),
)

urlpatterns += patterns('',    
    #account log- in/out/shakeitallabout
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/register/$', 'courses.views.register'),
    url(r'^accounts/created/$', 'courses.views.created'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.SITE_ROOT}),
    )

