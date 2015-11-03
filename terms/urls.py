#terms/urls.py
from django.conf.urls import url
from django.views.generic import TemplateView

from .import views

urlpatterns = [
    url(
        r'^$', 
        TemplateView.as_view(template_name='terms/terms_index.html'),
        name = 'terms_index'
    ),
    url(
        r'disclaimer/$',
        TemplateView.as_view(template_name='terms/terms_disclaimer.html'),
        name = 'terms_disclaimer'
    ),
    url(
        r'privacy/$',
        TemplateView.as_view(template_name='terms/terms_privacy.html'),
        name = 'terms_privacy'
    ),
    url(
        r'browsing/$', 
        TemplateView.as_view(template_name='terms/terms_browsing.html'),
        name = 'terms_browsing'
    ),
    url(
        r'enrolling/$', 
        TemplateView.as_view(template_name='terms/terms_enrolling.html'),
        name = 'terms_enrolling'
    ),
    url(
        r'creating/$',
        TemplateView.as_view(template_name='terms/terms_creating.html'),
        name = 'terms_creating'
    ),
]
