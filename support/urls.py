from django.conf.urls import patterns, url

urlpatterns = patterns ('support.views',
    url(r'^$', 'support')
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^thanks/$', 'direct_to_template', {'template': 'support/thanks.html'}),
)