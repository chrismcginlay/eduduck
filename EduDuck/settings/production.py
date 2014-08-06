#settings/prod.py
from base import *

DEBUG = False
TEMPLATE_DEBUG = False
#TEMPLATE_STRING_IF_INVALID = 'INVALID_EXPRESSION: %s'
TEMPLATE_STRING_IF_INVALID = 'TEMPLATE_ERROR'   #don't expose var names

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

