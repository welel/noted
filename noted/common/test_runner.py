from django.conf import settings
from django.test.runner import DiscoverRunner


class NotedDiscoverRunner(DiscoverRunner):
    def __init__(self, *args, **kwargs):
        settings.TEST_MODE = True
        settings.CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            }
        }
        super(NotedDiscoverRunner, self).__init__(*args, **kwargs)
