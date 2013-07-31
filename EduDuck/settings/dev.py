#settings/dev.py
from base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
TEMPLATE_STRING_IF_INVALID = 'INVALID_EXPRESSION: %s'

#django-registration needs an MTA. For development just use console
#smtp is the default, so in prod.py, EMAIL_BACKEND is commented out or missing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#INSTALLED_APPS += ("debug_toolbar", )
#INTERNAL_IPS = ("127.0.0.1", )
#MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ed_dev',
        'USER': 'ed_dev',                    
        'PASSWORD': 'quickquackquock',                 
        'HOST': '',
        'PORT': '',
#https://docs.djangoproject.com/en/dev/ref/databases/#creating-your-tables
#After your tables have been created, you should remove this option as it adds a query that is only needed during table creation to each database connection.
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
    },
# following is for resyncing database on staging server (would be better to 
# get python manage.py to read the staging.py config, as opposed to having this here.
#    'mysql_sync': {
#        'ENGINE': 'django.db.backends.mysql',
#        'HOST': '',
#	'NAME': 'eduduck',
#	'USER': 'put it back if you need to resync',
#	'PORT': '2369',
#	'PASSWORD': "put it back if you need to resync",
#        'OPTIONS': {
#            'init_command': 'SET storage_engine=INNODB',
#        },
#    },
}

#Not very secret SECRET_KEY. Just for dev. Staging and prod. use env var.
SECRET_KEY = '$9(8c0@dl9^0m@jautyrv&amp;y92!-ae6ymo+sl=&amp;^3ptfiw*ot7j'

# Fixture Directory - for development purposes, realoading test data
# after changes to models.
FIXTURE_DIRS = (
    os.path.join(SITE_ROOT, 'fixtures/')
)
