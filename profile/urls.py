from django.core.urlresolvers import reverse
from django.conf.urls import patterns, url

urlpatterns = patterns ('profile.views',
    url(r'^$', 'profile', name='profile'),
    url(r'^edit/$', 'edit', name='profile_edit'),
    url(r'^(?P<user_id>\d+)/public/$', 'public', name='profile_public'),
)

