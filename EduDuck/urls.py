#EduDuck/urls.py
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles import views as static_views
from django.views.generic import TemplateView

import attachment.urls
import checkout.urls
import courses.urls
import homepage.views
import interaction.urls
import lesson.urls
import outcome.urls
import profile.urls
import support.urls
import terms.urls

urlpatterns =  [
    url(r'^$', homepage.views.home, name='homepage'),
#    url(r'^search/', include('haystack.urls')),
    url(r'^about/$', TemplateView.as_view(template_name = 'about.html')),
    url(r'^priced_items/', include(checkout.urls, namespace='checkout')),
    url(r'^support/', include(support.urls)),
    url(r'^terms/', include(terms.urls, namespace='terms')),
    url(r'^lesson/(?P<lesson_id>\d+)/lint/', include(outcome.urls)),
    url(r'^courses/', include(courses.urls)),
    url(r'^interaction/', include(interaction.urls)),
    url(r'^accounts/profile/', include(profile.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^attachment/', include(attachment.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

