#settings/dev.py
from base import *

DEBUG = True
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'media'))
TEMPLATES[0]['OPTIONS'].update({
    'string_if_invalid':'Invalid Expression: %s',
    'debug':True
})

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

SOCIAL_AUTH_PIPELINE += (
    'social.pipeline.debug.debug',
)

