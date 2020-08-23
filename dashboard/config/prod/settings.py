import os
import sys
from os.path import join
import django_heroku
import dj_database_url

from dashboard.config.base.settings import *

INTERNAL_IPS=('127.0.0.1')

ROOT_URLCONF = 'dashboard.config.prod.urls'

WSGI_APPLICATION = 'dashboard.config.prod.wsgi.application'

DATABASES = {}

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

SECRET_KEY = os.environ['SECRET_KEY']

# If not using sqlite, move database settings to
# 'local_settings.py' outside of version control
try:
    from dashboard.config.local_settings import *
except ImportError:
    pass

INSTALLED_APPS += (
    'django_extensions'
)

# Test config tweaks/customizations
if 'test' in sys.argv:
    """
    #DATABASES['default'] = {'ENGINE':'django.db.backends.sqlite3'}
    #FIXTURE_DIRS = (
    #    PROJECT_ROOT + '/foo/bar/fixtures',
    #)
    """
    SOUTH_TESTS_MIGRATE = False

django_heroku.settings(locals())
