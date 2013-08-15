from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns ('bio.views',
    url(r'^$', 'bio'),
    url(r'^edit/$', 'edit'),
    url(r'^public/(?P<user_id>\d+)/$', 'public'),
)
