#settings/dev.py
from base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
TEMPLATE_STRING_IF_INVALID = 'INVALID_EXPRESSION: %s'

#django-registration needs an MTA. For development just use console
#smtp is the default, so in prod.py, EMAIL_BACKEND is commented out or missing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#INSTALLED_APPS += ("debug_toolbar", )
#INTERNAL_IPS = ("127.0.0.1", )
#MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(SITE_ROOT, 'EduDuck.db'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#Not very secret SECRET_KEY. Just for dev. Staging and prod. use env var.
SECRET_KEY = '$9(8c0@dl9^0m@jautyrv&amp;y92!-ae6ymo+sl=&amp;^3ptfiw*ot7j'

# Fixture Directory - for development purposes, realoading test data
# after changes to models.
FIXTURE_DIRS = (
    os.path.join(SITE_ROOT, 'fixtures/')
)
