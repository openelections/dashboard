import os
import sys
from os.path import join
import django_heroku
import dj_database_url

from dashboard.config.base.settings import *

DEBUG = True

INTERNAL_IPS=('127.0.0.1')

ROOT_URLCONF = 'dashboard.config.prod.urls'

WSGI_APPLICATION = 'dashboard.config.prod.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
    }
}

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

SECRET_KEY = os.environ['SECRET_KEY']
django_heroku.settings(locals())
