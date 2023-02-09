"""Common decorators for all applications."""

import functools
import logging

from django.http import HttpResponseBadRequest


def ajax_required(f):
    """AJAX request required decorator, allow only ajax requests.

    The decorator for views functions that require "X-Requested-With" header
    to be "XMLHttpRequest".
    """

    @functools.wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    return wrap
