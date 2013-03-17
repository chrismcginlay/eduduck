from django.conf.urls import patterns, url

urlpatterns = patterns('outcome.views',
    url(r'^lint/(?P<lint_id>\d+)/$', 'learning_intention'),
)
