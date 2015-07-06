#profile/urls.py
from django.core.urlresolvers import reverse
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    url(r'^edit/$', views.edit, name='profile_edit'),
    url(r'^(?P<user_id>\d+)/public/$', views.public, name='profile_public'),
]

