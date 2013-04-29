# Django settings for EduDuck project.

import os
import django

DEBUG = False

ADMINS = (
    ('Chris McGinlay', 'ctmcginlay@gmail.com'),
    ('Alan McGinlay', 'mrintegrity@gmail.com'),
)

MANAGERS = ADMINS

#get the path name to prepend to other settings
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))

SITE_ROOT = os.path.join(os.path.dirname(__file__), 
                                         os.path.pardir, 
                                         os.path.pardir)

# User Profile model 
AUTH_PROFILE_MODULE = 'bio.Bio'
LOGIN_REDIRECT_URL = '/courses/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
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
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
# Additional locations of static files

STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
    os.path.join(SITE_ROOT, 'EduDuck/static'),
)

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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'EduDuck.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'EduDuck.wsgi.application'

#TODO: Ensure templates aren't under docroot for production version
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
    'courses',
    'quiz',
    'support',
    'bio',
    'interaction',
    'outcome',
    'attachment',
    #following provides account activation via email via django-registration
    'registration',
)

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
#TODO uncomment when on Django 1.5
#        'require_debug_true': {
#            '()': 'django.utils.log.RequireDebugTrue'
#        }
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
            'filename': '/tmp/eduduck.log',
            'maxBytes': 10*2**20, #10 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'log_filedb': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/eduduck_db.log',
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
