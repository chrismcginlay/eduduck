#settings/staging.py
from base import *
import os
 
DEBUG = False 
TEMPLATE_DEBUG = False
TEMPLATE_STRING_IF_INVALID = 'TEMPLATE_ERROR'   #don't expose var names

ALLOWED_HOSTS = [
    'staging.eduduck.com',
    'eduduck.com', 
    'www.eduduck.com', 
]

# Make SECRET_KEY unique, and don't share it with anybody.
assert 'SECRET_KEY' in os.environ, 'SECRET_KEY missing from environment'
SECRET_KEY = os.environ['SECRET_KEY']

#MTA for django-registration
#smtp is the default, so for production, use default EMAIL_BACKEND 
assert 'EMAIL_HOST' in os.environ, 'EMAIL_HOST missing from environment'
assert 'EMAIL_PORT' in os.environ, 'EMAIL_PORT missing from environment'
assert 'EMAIL_HOST_USER' in os.environ, 'EMAIL_HOST_USER missing from environment'
assert 'EMAIL_HOST_PASSWORD' in os.environ, 'EMAIL_HOST_PASSWORD missing from environment'
assert 'EMAIL_USE_TLS' in os.environ, 'EMAIL_USE_TLS missing from environment'
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS']

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
