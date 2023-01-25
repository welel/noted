"""The project settings for local development."""

from .base import *


ALLOWED_HOSTS += ["127.0.0.1", "localhost"]

INSTALLED_APPS += ["rosetta"]
