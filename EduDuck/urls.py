from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EduDuck.views.home', name='home'),
    # url(r'^EduDuck/', include('EduDuck.foo.urls')),

    url(r'^courses/$', 'courses.views.index'),
    url(r'^courses/(?P<course_id>\d+)/$', 'courses.views.single'),

    url(r'^courses/(?P<course_id>\d+)/lesson/(?P<lesson_id>\d+)/$',
        'courses.views.lesson'),
    url(r'^courses/(?P<course_id>\d+)/quizzes/$', 'quiz.views.quiz_central'),    
    
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
