"""Loggining system for general, views and generic functions."""

import functools
import logging
import traceback

from django.db import transaction
from django.views import View


VIEW_LOG_TEMPLATE = "{name}\n{user}\n{method}\n{path}\n"
EXCEPTION_TEMPLATE = "{name}\n{msg}\n{args}\n{kwargs}\n{traceback}\n"

logger = logging.getLogger("exceptions")
view_logger = logging.getLogger("views.exceptions")


def logit(fn):
    """Logging decorator for general functions."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as error:
            logger.error(
                EXCEPTION_TEMPLATE.format(
                    name=fn.__name__,
                    msg=str(error),
                    args=str(args),
                    kwargs=(kwargs),
                    traceback=traceback.format_exc(),
                )
            )
            raise

    return wrapper


def logit_view(fn):
    """Logging decorator for a view function."""

    @functools.wraps(fn)
    def wrapper(request, *args, **kwargs):
        try:
            return fn(request, *args, **kwargs)
        except Exception as error:
            logger.error(
                VIEW_LOG_TEMPLATE.format(
                    name=fn.__name__,
                    user=request.user,
                    method=request.method,
                    path=request.path,
                )
                + EXCEPTION_TEMPLATE.format(
                    name=fn.__name__,
                    msg=str(error),
                    args=str(args),
                    kwargs=(kwargs),
                    traceback=traceback.format_exc(),
                )
            )
            raise

    return wrapper


def logit_class_method(fn):
    """Logging decorator for general class methods."""

    @functools.wraps(fn)
    def wrapper(instance, *args, **kwargs):
        try:
            return fn(instance, *args, **kwargs)
        except Exception as error:
            logger.error(
                EXCEPTION_TEMPLATE.format(
                    name=str(instance) + ": " + fn.__name__,
                    msg=str(error),
                    args=str(args),
                    kwargs=(kwargs),
                    traceback=traceback.format_exc(),
                )
            )
            raise

    return wrapper


def logit_generic_view_request(fn):
    """Logging decorator for a generic view function."""

    @functools.wraps(fn)
    def wrapper(view, request, *args, **kwargs):
        try:
            return fn(view, request, *args, **kwargs)
        except Exception as error:
            logger.error(
                VIEW_LOG_TEMPLATE.format(
                    name=str(view) + ": " + fn.__name__,
                    user=request.user,
                    method=request.method,
                    path=request.path,
                )
                + EXCEPTION_TEMPLATE.format(
                    name=str(view) + ": " + fn.__name__,
                    msg=str(error),
                    args=str(args),
                    kwargs=(kwargs),
                    traceback=traceback.format_exc(),
                )
            )
            raise

    return wrapper


class LoggingView(View):
    """A mixin that wraps a dispatch function of generic view with logging."""

    def dispatch(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                return super().dispatch(request, *args, **kwargs)
        except Exception as error:
            view_logger.error(
                VIEW_LOG_TEMPLATE.format(
                    name=str(self.__class__),
                    user=request.user,
                    method=request.method,
                    path=request.path,
                )
                + EXCEPTION_TEMPLATE.format(
                    name=str(self.__class__),
                    msg=str(error),
                    args=str(args),
                    kwargs=(kwargs),
                    traceback=traceback.format_exc(),
                )
            )
            raise
