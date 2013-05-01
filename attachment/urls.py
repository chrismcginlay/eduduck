from django.conf.urls import patterns, url

urlpatterns = patterns ('attachment.views',
    url(r'^$', 'view_metadata'),
)