from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns ('support.views',
    url(r'^$', 'support', name='support')
)

urlpatterns += patterns('',
    url(r'^thanks/$', TemplateView.as_view(
        template_name ='support/thanks.html')),
)
