#lesson/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<lesson_id>\d+)/$', views.visit, name='lesson_visit'),
    url(r'^(?P<lesson_id>\d+)/edit/$', views.edit, name='lesson_edit')
]
