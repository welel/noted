"""Common decorators for all applications."""

import functools
from typing import Callable, Literal

from django.http import HttpResponseBadRequest


def ajax_required(
    type: Literal["function", "method"] = "function"
) -> Callable:
    """AJAX request required decorator, allow only ajax requests.

    The decorator for views functions that require "X-Requested-With" header
    to be "XMLHttpRequest".
    """

    def decorator(fn) -> Callable:
        @functools.wraps(fn)
        def wrap(*args, **kwargs):
            if type == "method" and len(args) >= 2:
                request = args[1]
            else:
                request = args[0]
            if not request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return HttpResponseBadRequest()
            return fn(*args, **kwargs)

        return wrap

    return decorator
