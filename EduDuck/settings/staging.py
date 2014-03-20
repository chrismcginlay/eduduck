#settings/staging.py
from base import *
import os
 
DEBUG = False
TEMPLATE_DEBUG = DEBUG
#TEMPLATE_STRING_IF_INVALID = 'INVALID_EXPRESSION: %s'
TEMPLATE_STRING_IF_INVALID = 'TEMPLATE_ERROR'   #don't expose var names

ALLOWED_HOSTS = ['eduduck.com', 'www.eduduck.com', 'static.eduduck.com', 'media.eduduck.com']

# Make SECRET_KEY unique, and don't share it with anybody.
# see issue #43 for key generation method and location of Env Vars
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
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

assert 'EMAIL_PASSWORD' in os.environ, 'EMAIL_PASSWORD missing from environment'
#Fill in for given MTA
#EMAIL_HOST = 'a2s73.a2hosting.com'
EMAIL_HOST = 'mail.unpossible.info'
EMAIL_PORT = 25
#EMAIL_PORT = 465
EMAIL_HOST_USER = 'educk@unpossible.info'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
#EMAIL_USE_TLS = 'True'

assert 'DATABASE_NAME' in os.environ, 'DATABASE_NAME missing from environment'
assert 'DATABASE_USER' in os.environ, 'DATABASE_USER missing from environment'
assert 'DATABASE_PASSWORD' in os.environ, 'DATABASE_PASSWORD missing from environment'
assert 'DATABASE_PORT' in os.environ, 'DATABASE_PORT missing from environment'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'NAME': os.environ['DATABASE_NAME'],
        'PORT': os.environ['DATABASE_PORT'],
        'HOST': '',
        'OPTIONS': {
#            'read_default_file': '/etc/mysql/conf.d/eduduck_my.cnf',
        },
    },
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

WSGI_APPLICATION = "EduDuck.wsgi.application"
