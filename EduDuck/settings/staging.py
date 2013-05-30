#settings/staging.py
from base import *
import os
 
DEBUG = False
TEMPLATE_DEBUG = DEBUG
#TEMPLATE_STRING_IF_INVALID = 'INVALID_EXPRESSION: %s'
TEMPLATE_STRING_IF_INVALID = 'TEMPLATE_ERROR'   #don't expose var names

ALLOWED_HOSTS = ['eduduck.com', 'www.eduduck.com', 'static.eduduck.com', 'media.eduduck.com']

# Make SECRET_KEY unique, and don't share it with anybody.
# see issue #43 for key generation method.
assert 'SECRET_KEY' in os.environ, 'SECRET_KEY missing from environment'
SECRET_KEY = os.environ['SECRET_KEY']

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/www/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://static.eduduck.com/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://media.eduduck.com/'
MEDIA_ROOT = '/var/www/media/'

#django-registration needs an MTA. For development just use console
#smtp is the default, so for production, use default EMAIL_BACKEND 
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#Fill in for given MTA
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'bob'
EMAIL_HOST_PASSWORD = 'bobo'
EMAIL_USE_TLS = 'True'

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

WSGI_APPLICATION = "EduDuck.wsgi.application"
