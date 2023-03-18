"""The project settings for the production."""

from .base import *

from celery.schedules import crontab


DEBUG = False

ALLOWED_HOSTS = [
    "welel-noted.site",
    "www.welel-noted.site",
    get_env_variable("IP"),
]

CSRF_TRUSTED_ORIGINS = [
    "https://welel-noted.site",
    "http://welel-noted.site",
    "https://www.welel-noted.site",
    "http://www.welel-noted.site",
]

# Handles via nginx
# SECURE_SSL_REDIRECT = True

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": get_env_variable("REDIS_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CELERY_BROKER_URL = get_env_variable("REDIS_LOCATION")
CELERY_RESULT_BACKEND = get_env_variable("REDIS_LOCATION")
CELERY_BEAT_SCHEDULE = {
    "telegram_report_task": {
        "task": "common.tasks.telegram_report_task",
        "schedule": crontab(minute=45, hour=21 - 3),
    },
}
