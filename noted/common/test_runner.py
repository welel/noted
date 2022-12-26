from django.conf import settings
from django.test.runner import DiscoverRunner


class NotedDiscoverRunner(DiscoverRunner):
    def __init__(self, *args, **kwargs):
        settings.TEST_MODE = True
        super(NotedDiscoverRunner, self).__init__(*args, **kwargs)
