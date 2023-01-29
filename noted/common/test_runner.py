from django.conf import settings
from django.test.runner import DiscoverRunner


class NotedDiscoverRunner(DiscoverRunner):
    """Sets config settings to the test mode."""

    def __init__(self, *args, **kwargs):
        settings.TEST_MODE = True
        settings.CACHES = {
            "default": {
                "BACKEND": "common.cache.RedisDummyCache",
            }
        }
        super(NotedDiscoverRunner, self).__init__(*args, **kwargs)
