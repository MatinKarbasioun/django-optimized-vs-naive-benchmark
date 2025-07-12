import dj_database_url
from decouple import Config, RepositoryEnv, Csv

from .base import *


config = Config(RepositoryEnv('.env.dev'))

INSTALLED_APPS += [
    'debug_toolbar'
    ]

SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = config("DEBUG", cast=bool, default=True)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default='127.0.0.1, localhost',cast=Csv())

ROOT_URLCONF = 'crm_naive.urls.dev'

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1"
]

DATABASES = {
    'default': dj_database_url.parse(
        config('DATABASE_URL'),
        conn_health_checks=False
    )
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}