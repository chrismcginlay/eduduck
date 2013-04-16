#settings/prod.py
from base import *

#django-registration needs an MTA. For development just use console
#smtp is the default, so for production, use default EMAIL_BACKEND 
#EMAIL_BACKEND = 

#Fill in for given MTA
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'bob'
EMAIL_HOST_PASSWORD = 'bobo'
EMAIL_USE_TLS = 'True'