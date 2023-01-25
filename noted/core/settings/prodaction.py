"""The project settings for the prodaction."""

from .base import *

DEBUG = False

ALLOWED_HOSTS = ["welel-noted.site", "www.welel-noted.site", os.getenv("IP")]

CSRF_TRUSTED_ORIGINS = [
    "https://welel-noted.site",
    "http://welel-noted.site",
    "https://www.welel-noted.site",
    "http://www.welel-noted.site",
]

# Handles via nginx
# SECURE_SSL_REDIRECT = True

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
