from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

#TODO decouple quiz app URLs from courses - see p38

urlpatterns = patterns('django.views.generic.simple',
    (r'^$',    'direct_to_template', {'template': 'home.html'}),
    (r'^about/$', 'direct_to_template', {'template': 'about.html'}),
)

urlpatterns += patterns('',
    # Examples:
    # url(r'^$', 'EduDuck.views.home', name='home'),
    # url(r'^EduDuck/', include('EduDuck.foo.urls')),

    url(r'^courses/$', 'courses.views.index'),
    url(r'^courses/(?P<course_id>\d+)/$', 'courses.views.single'),

    url(r'^courses/(?P<course_id>\d+)/lesson/(?P<lesson_id>\d+)/$',
        'courses.views.lesson'),
    #TODO consider deletion of item below
    url(r'^courses/(?P<course_id>\d+)/quizzes/$', 'quiz.views.quizzes'),    
    
    #temporary question handler
    url(r'^questions/$', 'quiz.views.questions'),
    url(r'^question_add/$', 'quiz.views.question_add'),    
    url(r'^question_edit/(?P<question_id>\d+)/$', 'quiz.views.question_edit'),
    url(r'^question_delete/(?P<question_id>\d+)/$', 'quiz.views.question_delete'),
    
    #temporary answer handler
    url(r'^answers/$', 'quiz.views.answers'),
    url(r'^answer_add/$', 'quiz.views.answer_add'),    
    url(r'^answer_edit/(?P<answer_id>\d+)/$', 'quiz.views.answer_edit'),
    url(r'^answer_delete/(?P<answer_id>\d+)/$', 'quiz.views.answer_delete'),

    #temporary quiz handler
    url(r'^quizzes/$', 'quiz.views.quizzes'),
    url(r'^quiz_add/$', 'quiz.views.quiz_add'),    
    url(r'^quiz_edit/(?P<quiz_id>\d+)/$', 'quiz.views.quiz_edit'),
    url(r'^quiz_delete/(?P<quiz_id>\d+)/$', 'quiz.views.quiz_delete'),
    url(r'^quiz_take/(?P<quiz_id>\d+)/$', 'quiz.views.quiz_take2'),

    #testing only
    url(r'^questiontest/$', 'quiz.views.testquestion'),    
    
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/register/$', 'courses.views.register'),
    url(r'^accounts/created/$', 'courses.views.created'),

    #requires pip install django-registration,  if we want to use it
    #url(r'^accounts/', include('registration.backends.simple.urls')),
    #url(r'^accounts/', include('registration.backends.default.urls')),

    # following includes regex for username to include .@+- characters
    # TODO: truncate this to ^users/ since the view handles username
    url(r'^users/$', 'courses.views.user_profile'),
    #url(r'^users/(?P<username>[\w.@+-]+)/$', 'courses.views.user_profile'),
       
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.SITE_ROOT}),
    )

