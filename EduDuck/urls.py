from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

#TODO decouple quiz app URLs from eduduck platform #9
#TODO decouple courses app URLs from eduduck platform #9

urlpatterns = patterns('django.views.generic.simple',
    (r'^about/$', 'direct_to_template', {'template': 'about.html'}),
)

urlpatterns += patterns('',
    url(r'^support/', include('support.urls')),
    url(r'^lesson/(?P<lesson_id>\d+)/lint/', include('outcome.urls')),
    url(r'^interaction/', include('interaction.urls')),
    url(r'^accounts/bio/', include('bio.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
        
urlpatterns += patterns('courses.views',
    url(r'^$', 'index'),
    url(r'^courses/$', 'index'),
    url(r'^courses/(?P<course_id>\d+)/$', 'single'),
    url(r'^courses/(?P<course_id>\d+)/lesson/(?P<lesson_id>\d+)/$',
        'lesson'),
)
 
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
    url(r'^quiz_take/(?P<quiz_id>\d+)/$', 'quiz_take'),
    url(r'^quiz_results/(?P<quiz_id>\d+)/$', 'quiz_results'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.SITE_ROOT}),
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT,}),
    )

