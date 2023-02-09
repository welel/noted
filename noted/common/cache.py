import functools

from django.core.cache import cache
from django.core.cache.backends.dummy import DummyCache
from django.db.models import QuerySet


class RedisDummyCache(DummyCache):
    def delete_pattern(self, *args, **kwargs):
        pass


def cache_queryset(time: int) -> QuerySet:
    """A decorator for caching function result by a function name as a key.

    Caches result a function by a function name.

    Args:
        time: Time in seconds for caching result.
    """

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            key = fn.__name__
            queryset = cache.get(key)
            if not queryset:
                queryset = fn(*args, **kwargs)
                cache.set(key, queryset, time)
            return queryset

        return wrapper

    return decorator
