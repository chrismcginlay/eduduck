from django.core.urlresolvers import reverse
from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns ('bio.views',
    url(r'^$', 'bio'),
    url(r'^edit/$', 'edit'),
    url(r'^public/(?P<user_id>\d+)/$', 'public'),
)

urlpatterns += patterns( '',
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', { 
        'template_name': 'bio/password_change_form.html',
        'post_change_redirect': 'bio/password_change_done.html' }),
    url(r'^password_change/done/$', 
        'django.contrib.auth.views.password_change_done', { 
        'template_name': 'bio/password_change_done.html', }),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {
        'template_name': 'bio/password_reset_form.html',
        'post_reset_redirect': 'bio/password_reset_done.html', }),
    url(r'^password_reset_confirm/$', 
        'django.contrib.auth.views.password_reset_confirm', {
        'template_name': 'bio/password_reset_confirm', }),
    url(r'^password_reset_done/$', 
        'django.contrib.auth.views.password_reset_done', { 
        'template_name': 'bio/password_reset_done.html',}),

    # url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    # url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     'django.contrib.auth.views.password_reset_confirm',
    #     name='password_reset_confirm'),
    # url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

)
