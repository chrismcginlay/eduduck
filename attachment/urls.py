from django.conf.urls import patterns, url

urlpatterns = patterns ('',
    url(r'^(?P<att_id>\d+)/metadata/$', 'attachment.views.metadata'),
)