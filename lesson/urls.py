# urls for lesson app
from django.conf.urls import patterns, url

urlpatterns = patterns('lesson.views', 
    url(r'^(?P<lesson_id>\d+)/$', 'visit', name='lesson_visit'),
    url(r'^(?P<lesson_id>\d+)/edit/$', 'edit', name='lesson_edit')
)
