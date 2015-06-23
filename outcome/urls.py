from django.conf.urls import patterns, url

urlpatterns = patterns('outcome.views',
    url(
        r'^(?P<learning_intention_id>\d+)/$', 
        'learning_intention',
        name='learning_intention'),
    url(r'^(?P<learning_intention_id>\d+)/edit/$', 'edit', name='lint_edit'),
)
