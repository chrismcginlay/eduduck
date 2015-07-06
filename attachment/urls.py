#attachment/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<att_id>\d+)/metadata/$', views.metadata),
]
