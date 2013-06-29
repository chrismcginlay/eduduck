#settings/temp_deploy.py

#Use this if you need to run manage.py syncdb from shell to create database tables in MySQL
#with proper secrets loaded (as they won't be available, since apache loads them from its environment variables

from base import *
import os
 
DEBUG = True
TEMPLATE_DEBUG = DEBUG
#TEMPLATE_STRING_IF_INVALID = 'INVALID_EXPRESSION: %s'
TEMPLATE_STRING_IF_INVALID = 'TEMPLATE_ERROR'   #don't expose var names

ALLOWED_HOSTS = ['eduduck.com', 'www.eduduck.com', 'static.eduduck.com', 'media.eduduck.com']

# Make SECRET_KEY unique, and don't share it with anybody.
# see issue #43 for key generation method and location of Env Vars
SECRET_KEY=''

DATABASE_PASSWORD=''
DATABASE_USER=''
DATABASE_NAME=''
DATABASE_PORT=''

EMAIL_PASSWORD=''


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

#assert 'EMAIL_PASSWORD' in os.environ, 'EMAIL_PASSWORD missing from environment'
#Fill in for given MTA
EMAIL_HOST = 'a2s73.a2hosting.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'educk@unpossible.info'
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
EMAIL_USE_TLS = 'True'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
	'USER': DATABASE_USER,
   	'PASSWORD': DATABASE_PASSWORD,
	'NAME': DATABASE_NAME,
	'PORT': DATABASE_PORT,
        'HOST': '',
        'OPTIONS': {
#            'read_default_file': '/etc/mysql/conf.d/eduduck_my.cnf',
        },
    },
}

WSGI_APPLICATION = "EduDuck.wsgi.application"
