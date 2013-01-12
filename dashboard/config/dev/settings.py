from dashboard.config.base.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS=('127.0.0.1')

ROOT_URLCONF = 'dashboard.config.dev.urls'

WSGI_APPLICATION = 'dashboard.config.dev.wsgi.application'

# If we use anything other than sqlite, move database settings in 
# 'local_settings.py' file outside of version control
try:
    from dashboard.config.dev.local_settings import *
except ImportError:
    pass

# Test config tweaks/customizations
"""
if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE':'django.db.backends.sqlite3'}
    FIXTURE_DIRS = (
        PROJECT_ROOT + '/foo/bar/fixtures',
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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
