#terms/urls.py
from django.conf.urls import url
from django.views.generic import TemplateView

from .import views

urlpatterns = [
    url(
        r'^$', 
        TemplateView.as_view(template_name='terms/terms_index.html'
    )),
    url(
        r'privacy/$',
        TemplateView.as_view(template_name='terms/terms_privacy.html'
    )),
    url(
        r'browsing/$', 
        TemplateView.as_view(template_name='terms/terms_browsing.html'
    )),
    url(
        r'enrolling/$', 
        TemplateView.as_view(template_name='terms/terms_enrolling.html'
    )),
    url(
        r'creating/$',
        TemplateView.as_view(template_name='terms/terms_creating.html'
    )),
]
