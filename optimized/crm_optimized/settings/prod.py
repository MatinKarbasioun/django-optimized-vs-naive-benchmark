import dj_database_url
from decouple import Config, RepositoryEnv, Csv

from .base import *

config = Config(RepositoryEnv('.env'))

SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

ROOT_URLCONF = 'crm_optimized.urls'

DATABASES = {
    'default': dj_database_url.parse(
        config('DATABASE_URL'),
        conn_health_checks=True,
        conn_max_age=60
    )
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
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