#settings/prod.py
from base import *

# Make SECRET_KEY unique, and don't share it with anybody.
# see issue #43 for key generation method.
assert 'SECRET_KEY' in os.environ, 'SECRET_KEY missing from environment'
SECRET_KEY = os.environ['SECRET_KEY']

#django-registration needs an MTA. For development just use console
#smtp is the default, so for production, use default EMAIL_BACKEND 
#EMAIL_BACKEND = 

#Fill in for given MTA
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'bob'
EMAIL_HOST_PASSWORD = 'bobo'
EMAIL_USE_TLS = 'True'

"""
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
"""