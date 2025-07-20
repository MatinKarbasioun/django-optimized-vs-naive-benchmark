import dj_database_url
from decouple import Config, RepositoryEnv, Csv

from .base import *

config = Config(RepositoryEnv('.env'))

SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

ROOT_URLCONF = 'crm_optimized.urls.urls'

DATABASES = {
    'default': dj_database_url.parse(
        config('DATABASE_URL'),
        conn_health_checks=True,
        conn_max_age=60
    )
}

CACHES = {
    "default": {
        "BACKEND": config("CACHE_BACKEND"),
        "LOCATION": config("CACHE_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": config("CLIENT_CLASS"),
        },
        "TIMEOUT": config("CACHE_TIMEOUT", cast=int, default=300),
    }
}

LOGGING['loggers'].update({
    'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
})

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False