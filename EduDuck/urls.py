from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'homepage.views.home', name='homepage'),
#    url(r'^search/', include('haystack.urls')),
    url(r'^about/$', TemplateView.as_view(template_name = 'about.html')),
    url(r'^support/', include('support.urls')),
    url(r'^lesson/(?P<lesson_id>\d+)/lint/', include('outcome.urls')),
    url(r'^courses/', include('courses.urls')),
    url(r'^interaction/', include('interaction.urls')),
    url(r'^accounts/profile/', include('profile.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url('', include('social.apps.django_app.urls', 
        namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^attachment/', include('attachment.urls')),
)
 
##temporary question handler
#urlpatterns += patterns('quiz.views',
    #url(r'^questions/$', 'questions'),
    #url(r'^question_add/$', 'question_add'),    
    #url(r'^question_edit/(?P<question_id>\d+)/$', 'question_edit'),
    #url(r'^question_delete/(?P<question_id>\d+)/$', 'question_delete'),

    ##temporary answer handler
    #url(r'^answers/$', 'answers'),
    #url(r'^answer_add/$', 'answer_add'),    
    #url(r'^answer_edit/(?P<answer_id>\d+)/$', 'answer_edit'),
    #url(r'^answer_delete/(?P<answer_id>\d+)/$', 'answer_delete'),

    ##temporary quiz handler
    #url(r'^quizzes/$', 'quizzes'),
    #url(r'^quiz_add/$', 'quiz_add'),    
    #url(r'^quiz_edit/(?P<quiz_id>\d+)/$', 'quiz_edit'),
    #url(r'^quiz_delete/(?P<quiz_id>\d+)/$', 'quiz_delete'),
    #url(r'^quiz_take/(?P<quiz_id>\d+)/$', 'quiz_take'),
    #url(r'^quiz_results/(?P<quiz_id>\d+)/$', 'quiz_results'),
#)

if settings.DEBUG:
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.SITE_ROOT}),
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT,}),
    )

