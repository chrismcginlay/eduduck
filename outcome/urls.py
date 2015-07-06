#outcome/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^(?P<learning_intention_id>\d+)/$', 
        views.learning_intention,
        name='learning_intention'
    ),
    url(
        r'^(?P<learning_intention_id>\d+)/edit/$',
        views.edit,
        name='lint_edit'
    ),
]
