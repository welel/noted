"""Common decorators for all applications."""

from django.http import HttpResponseBadRequest


def ajax_required(f):
    """AJAX request required decorator, allow only ajax requests."""

    def wrap(request, *args, **kwargs):
        if not request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
