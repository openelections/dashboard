from os.path import abspath, dirname, join

PROJECT_ROOT = abspath(join(dirname(__file__), "..", ".."))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('OpenElections Admin', 'openelections@gmail.com'),
)
MANAGERS = ADMINS

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

# Below requires PROJECT_ROOT to be on PYTHONPATH
ROOT_URLCONF = 'dashboard.config.base.urls'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/var/www/dashboard/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Statics are collected out of /static/ directories in each app
# via management command. Below settings control where an app's static files
# are moved to, for example: /var/www/static/project/, which would then
# be served up at the STATIC_URL such as
# http://my.mediaserver.com/apps/static/project/
STATIC_URL = '/static/'

STATIC_ROOT = '/var/www/dashboard/static'

STATICFILES_DIRS = (
    join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_DIRS = (
    join(PROJECT_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Project apps must precede
    'grappelli',
    'django.contrib.admin',
    'dashboard.apps.hub',
)

GRAPPELLI_ADMIN_TITLE = 'The OpenElections Project'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'DEBUG',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
