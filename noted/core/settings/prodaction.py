"""The project settings for the prodaction."""

from .base import *

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
