#interaction/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^attachment/(?P<att_id>\d+)/download/$',
        views.attachment_download,
        name='attachment_download'
    ),
    url(
        r'^user/(?P<user_id>\d+)/course/(?P<course_id>\d+)/$',
        views.usercourse_single,
        name='usercourse_single'
    ),
    url(
        r'^user/(?P<user_id>\d+)/lesson/(?P<lesson_id>\d+)/$',
        views.userlesson_single,
        name='userlesson_single'
    ),
    url(
        r'^user/(?P<user_id>\d+)/learningintentiondetail/(?P<lid_id>\d+)/$',
        views.userlearningintentiondetail_single,
        name='userlearningintentiondetail_single'
    ),
    url(
        r'^learningintentiondetail/(?P<lid_id>\d+)/status/$',
        views.ajax_learningintentiondetail_status,
        name='ajax_learningintentiondetail_status'
    ),
    url(r'^learningintentiondetail/(?P<lid_id>\d+)/cycle/$',
        views.userlearningintentiondetail_cycle,
        name='userlearningintentiondetail_cycle'
    ),
    url(r'^learningintentiondetail/(?P<lid_id>\d+)/progress/$',
        views.userlearningintention_progress_bar,
        name='userlearningintention_progress_bar'
    ),
]
