from django.conf.urls import patterns, url

urlpatterns = patterns('outcome.views',
    url(r'^(?P<learning_intention_id>\d+)/$', 'learning_intention'),
)
