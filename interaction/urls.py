from django.conf.urls import patterns, url

urlpatterns = patterns('interaction.views',
    url(r'^user/(?P<user_id>\d+)/course/(?P<course_id>\d+)/$', 'usercourse_single'),
    url(r'^user/(?P<user_id>\d+)/lesson/(?P<lesson_id>\d+)/$', 'userlesson_single'),
    url(r'^user/(?P<user_id>\d+)/successcriterion/(?P<sc_id>\d+)/$', 'usersuccesscriterion_single')    
)
