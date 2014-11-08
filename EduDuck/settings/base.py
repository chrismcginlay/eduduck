# Django settings for EduDuck project.

import os
import django
from django.conf import global_settings

DEBUG = False

ADMINS = (
    ('Chris McGinlay', 'ctmcginlay@gmail.com'),
    ('Alan McGinlay', 'mrintegrity@gmail.com'),
)

MANAGERS = ADMINS

#get the path name to prepend to other settings
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))

SITE_ROOT = os.path.normpath(
    os.path.join(os.path.realpath(__file__), "../../../"))

LOGIN_REDIRECT_URL = '/accounts/bio/'

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'UTC'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

#https://docs.djangoproject.com/en/dev/ref/contrib/sites/?from=olddocs
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.normpath(os.path.join(SITE_ROOT, '../static/'))

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL ='/static/'

# Additional locations of static files
STATICFILES_DIRS = (os.path.join(SITE_ROOT, 'static'),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'core.context_processors.git_branch_render',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.TimezoneMiddleware',
)

ROOT_URLCONF = 'EduDuck.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'EduDuck.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

#django-registration https://bitbucket.org/ubernostrum/django-registration
#This allows new users 7 days to activate new accounts
ACCOUNT_ACTIVATION_DAYS = 7
#Set following to False to disable registration.
REGISTRATION_OPEN = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    #Temporarily disabling haystack - 'six' package/bundled conflict?
    #django-haystack via elasticsearch backend
    #'haystack',

    #eduduck apps
    'attachment',
    'bio',
    'courses',
    'interaction',
    'homepage',
    'lesson',
    'outcome',
    'quiz',
    'support',
    'video'
)

# See http://django-haystack.readthedocs.org/en/latest/tutorial.html#simple
# and override this in staging.py and production.py
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
#this is only here since I can't get python manage.py to read this config (handled via wsgi)
#use via python manage.py rebuild_index --using='forcron'
    'forcron': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
            },
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
        },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/eduduck.log',
            'maxBytes': 10*2**20, #10 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'log_filedb': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/eduduck_db.log',
            'maxBytes': 10*2**20, #10 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['log_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['log_filedb', 'console'],
            'propagate': False,
            'level': 'DEBUG',
        },
    }
}
