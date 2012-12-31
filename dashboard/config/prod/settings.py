from dashboard.config.base.settings import *

INTERNAL_IPS=('127.0.0.1')

ROOT_URLCONF = 'dashboard.config.prod.urls'

WSGI_APPLICATION = 'dashboard.config.prod.wsgi.application'

# Default to sqlite
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'dashboard.db'),
        'USER':  '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# If not using sqlite, move database settings to 
# 'local_settings.py' outside of version control
try:
    from dashboard.config.prod.local_settings import *
except ImportError:
    pass

INSTALLED_APPS += (
    #'debug_toolbar',
    'django_extensions',
    'south',
    #'test_utils',
)
