import sys
from os.path import join

from dashboard.config.base.settings import *

INTERNAL_IPS=('127.0.0.1')

ROOT_URLCONF = 'dashboard.config.prod.urls'

WSGI_APPLICATION = 'dashboard.config.prod.wsgi.application'

# Default to sqlite
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.sqlite3',
        'NAME': join(PROJECT_ROOT, 'dashboard.db'),
        'USER':  '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# If not using sqlite, move database settings to
# 'local_settings.py' outside of version control
try:
    from dashboard.config.local_settings import *
except ImportError:
    pass

INSTALLED_APPS += (
    #'debug_toolbar',
    'django_extensions',
    'south',
    #'test_utils',
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
