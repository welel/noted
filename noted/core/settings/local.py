"""The project settings for local development."""

from .base import *


ALLOWED_HOSTS += ["127.0.0.1", "localhost"]

INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS += ["rosetta", "debug_toolbar"]

MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

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
