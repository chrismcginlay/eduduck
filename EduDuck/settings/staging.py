#:settings/staging.py
import os.path
from base import *

DEBUG = False 
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, '../media'))
STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, '../static'))
TEMPLATES[0]['OPTIONS'].update({
    'string_if_invalid':'Sorry, there\'s been a template error.',
    'debug':False
})

ALLOWED_HOSTS = [
    'staging.eduduck.com',
    'eduduck.com', 
    'www.eduduck.com', 
]

#SESSION_COOKIE_SECURE = True
#SESSION_COOKIE_DOMAIN = '.eduduck.com'
#CSRF_COOKIE_SECURE = True

# Make SECRET_KEY unique, and don't share it with anybody.
assert 'SECRET_KEY' in os.environ, 'SECRET_KEY missing from environment'
SECRET_KEY = os.environ['SECRET_KEY']

#MTA
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

#Stripe TEST keys
assert 'STRIPE_SECRET_KEY' in os.environ, 'STRIPE_SECRET_KEY(TEST) missing'
assert 'STRIPE_PUBLISHABLE_KEY' in os.environ, 'STRIPE_PUBLISHABLE_KEY(TEST) missing'

STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
STRIPE_PUBLISHABLE_KEY = os.environ['STRIPE_PUBLISHABLE_KEY']

#assert 'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY' in os.environ, 'PSA GOOGLE KEY missing'
#assert 'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET' in os.environ, 'PSA GOOGLE SECRET missing'
#assert 'SOCIAL_AUTH_FACEBOOK_KEY' in os.environ, 'PSA FACEBOOK KEY missing'
#assert 'SOCIAL_AUTH_FACEBOOK_SECRET' in os.environ, 'PSA FACEBOOK SECRET missing'
#assert 'SOCIAL_AUTH_TWITTER_KEY' in os.environ, 'PSA TWITTER KEY missing'
#assert 'SOCIAL_AUTH_TWITTER_SECRET' in os.environ, 'PSA TWITTER SECRET missing'

#SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
#SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
#SOCIAL_AUTH_FACEBOOK_KEY = os.environ['SOCIAL_AUTH_FACEBOOK_KEY']
#SOCIAL_AUTH_FACEBOOK_SECRET = os.environ['SOCIAL_AUTH_FACEBOOK_SECRET']
#SOCIAL_AUTH_FACEBOOK_SCOPE = ['email'] 
#SOCIAL_AUTH_TWITTER_KEY = os.environ['SOCIAL_AUTH_TWITTER_KEY']
#SOCIAL_AUTH_TWITTER_SECRET = os.environ['SOCIAL_AUTH_TWITTER_SECRET']

assert 'DATABASE_NAME' in os.environ, 'DATABASE_NAME missing from environment'
assert 'DATABASE_USER' in os.environ, 'DATABASE_USER missing from environment'
assert 'DATABASE_PASSWORD' in os.environ, 'DATABASE_PASSWORD missing from environment'
assert 'DATABASE_PORT' in os.environ, 'DATABASE_PORT missing from environment'

dbpw = os.environ['DATABASE_PASSWORD']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': dbpw,
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
