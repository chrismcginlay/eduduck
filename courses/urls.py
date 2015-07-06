#courses/urls.py
from django.conf.urls import include, url

from . import views
import lesson.urls

urlpatterns = [
    url(r'^$', views.index, name='course_index'),
    url(r'^(?P<course_id>\d+)/edit/$', views.edit, name='course_edit'),
    url(r'^(?P<course_id>\d+)/enrol/$', views.enrol, name='course_enrol'),
    url(r'^(?P<course_id>\d+)/$', views.single, name='course_single'),
    url(r'^create/$', views.create, name='course_create'),
    url(r'^(?P<course_id>\d+)/lesson/', include(lesson.urls)),
]

