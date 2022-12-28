import functools

from django.core.cache import cache
from django.conf import settings
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.cache import get_cache_key
from django.urls import reverse


def cache_queryset(time: int) -> QuerySet:
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
