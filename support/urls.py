from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.support, name='support'),
    url(
        r'^thanks/$',
        TemplateView.as_view(template_name ='support/thanks.html')),
]
