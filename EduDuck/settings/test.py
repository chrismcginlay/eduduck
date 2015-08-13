#settings/test.py
from base import *

DEBUG = True
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'media'))
STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'static'))
TEMPLATES[0]['OPTIONS'].update({
    'string_if_invalid':'Invalid Expression: %s',
    'debug':True
})

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/eduduck-messages'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(BASE_DIR, 'Testing.db'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#Not very secret SECRET_KEY. Just for dev. Staging and prod. use env var.
SECRET_KEY = '$9(8c0@dl9^0m@jautyrv&amp;y92!-ae6ymo+sl=&amp;^3ptfiw*ot7j'

FIXTURE_DIRS = (os.path.join(BASE_DIR, 'functional_tests/fixtures/'),)
SOCIAL_AUTH_PIPELINE += (
    'social.pipeline.debug.debug',
)

INSTALLED_APPS += ('checkout.tests.dummy_app',)
