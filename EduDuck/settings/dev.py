#settings/dev.py
from base import *

DEBUG = True
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'media'))
TEMPLATE_DEBUG = DEBUG
TEMPLATE_STRING_IF_INVALID = 'INVALID_EXPRESSION: %s'

#django-registration needs an MTA. For development just use console
#smtp is the default, so in prod.py, EMAIL_BACKEND is commented out or missing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#Not very secret SECRET_KEY. Just for dev. Staging and prod. use env var.
SECRET_KEY = '$9(8c0@dl9^0m@jautyrv&amp;y92!-ae6ymo+sl=&amp;^3ptfiw*ot7j'

# Again, staging and production use more secure environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'ed_dev',
        'PASSWORD': 'quickquackquock',
        'NAME': 'ed_dev',
    }
}

INSTALLED_APPS += ("debug_toolbar", )
#INTERNAL_IPS = ("127.0.0.1", )
#MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

# Fixture Directory - for development purposes, reloading test data
# after changes to models.
FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures/')
)

SOCIAL_AUTH_PIPELINE += (
    'social.pipeline.debug.debug',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '882717436949-lb365iq5sb5aeo3l7e8u132bkld9opsm.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'LGVtAs_8PG6hHhD_VdihoIgt'
SOCIAL_AUTH_FACEBOOK_KEY = '307437099449489'
SOCIAL_AUTH_FACEBOOK_SECRET = '4f4a3f5309d729d7e636538022e5881e'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']


