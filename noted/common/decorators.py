from django.http import HttpResponseBadRequest


def ajax_required(f):
    """A decorator that allows only ajax request.

    It is a wrap function that returns an HttpResponseBadRequest
    object (HTTP 400 code) if the request is not AJAX. Otherwise,
    it returns the decorated function.
    """
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__= f.__doc__
    wrap.__name__= f.__name__
    return wrap
