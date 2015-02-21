from django.conf.urls import patterns, url

urlpatterns = patterns('interaction.views',
    url(r'^attachment/(?P<att_id>\d+)/download/$',
        'attachment_download', 
        name='attachment_download'),
    url(r'^user/(?P<user_id>\d+)/courses/(?P<course_id>\d+)/$', 
        'usercourse_single',
        name='usercourse_single'),
    url(r'^user/(?P<user_id>\d+)/lesson/(?P<lesson_id>\d+)/$',
        'userlesson_single',
        name='userlesson_single'),
    url(r'^user/(?P<user_id>\d+)/learningintentiondetail/(?P<lid_id>\d+)/$',
        'userlearningintentiondetail_single',
        name='userlearningintentiondetail_single'),   
    url(r'^learningintentiondetail/(?P<lid_id>\d+)/cycle/$',
        'userlearningintentiondetail_cycle',
        name='userlearningintentiondetail_cycle'),
    url(r'^learningintentiondetail/(?P<lid_id>\d+)/progress/$',
        'userlearningintention_progress_bar',
        name='userlearningintention_progress_bar'),
)
