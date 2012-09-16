from config.base.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS=('127.0.0.1')

ROOT_URLCONF = 'config.dev.urls'

WSGI_APPLICATION = 'config.dev.openelex_dash_wsgi.application'

# Default to sqlite
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.sqlite3', #'django.db.backends.postgresql_psycopg2',
        'NAME': os.path.join(PROJECT_ROOT, 'dashboard.db'),
        'USER':  '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# If we use anything other than sqlite, move database settings in 
# 'db_settings.py' file outside of version control
try:
    from config.prod.db_settings import DATABASES
except ImportError:
    pass

# Test config tweaks/customizations
"""
if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE':'django.db.backends.sqlite3'}
    FIXTURE_DIRS = (
        PROJECT_ROOT + '/apps/election_results/ap/tests/fixtures',
    )
    SOUTH_TESTS_MIGRATE = False
"""

INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
    'south',
    'test_utils',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    #'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    #'EXTRA_SIGNALS': ['myproject.signals.MySignal'],
    #'HIDE_DJANGO_SQL': False,
    #'TAG': 'div',
}
