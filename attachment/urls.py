from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns ('attachment.views',
    url(r'^$', 'view_metadata'),
    url(r'^(?P<att_id>\d+)_(?P<att_code>\w+)/download/$', 'download'),
)