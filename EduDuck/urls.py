#EduDuck/urls.py
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles import views as static_views
from django.views.generic import TemplateView

import attachment.urls
import checkout.urls
import courses.urls
import homepage.views
import interaction.urls
import lesson.urls
import outcome.urls
import profile.urls
import support.urls
import terms.urls

urlpatterns =  [
    url(r'^$', homepage.views.home, name='homepage'),
#    url(r'^search/', include('haystack.urls')),
    url(r'^about/$', TemplateView.as_view(template_name = 'about.html')),
    url(r'^priced_items/', include(checkout.urls, namespace='checkout')),
    url(r'^support/', include(support.urls)),
    url(r'^terms/', include(terms.urls, namespace='terms')),
    url(r'^lesson/(?P<lesson_id>\d+)/lint/', include(outcome.urls)),
    url(r'^courses/', include(courses.urls)),
    url(r'^interaction/', include(interaction.urls)),
    url(r'^accounts/profile/', include(profile.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^attachment/', include(attachment.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

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

