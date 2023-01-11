"""Common decorators for all applications."""

import functools
import logging

from django.http import HttpResponseBadRequest

from common.logging import VIEW_LOG_TEMPLATE


logger = logging.getLogger("django.request")


def ajax_required(f):
    """AJAX request required decorator, allow only ajax requests.

    The decorator for views functions that require "X-Requested-With" header
    to be "XMLHttpRequest".
    """

    @functools.wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.headers.get("X-Requested-With") == "XMLHttpRequest":
            logger.error(
                VIEW_LOG_TEMPLATE.format(
                    name=f.__name__,
                    user=request.user,
                    method=request.method,
                    path=request.path,
                )
                + "Bad ajax request"
            )
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    return wrap
