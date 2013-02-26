from django.conf.urls import patterns, url

urlpatterns = patterns('interaction.views',
    url(r'^user/(?P<user_id>\d+)/course/(?P<course_id>\d+)/$', 'usercourse_single')
)
