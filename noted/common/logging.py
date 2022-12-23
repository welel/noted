import functools
import logging
import traceback

from django.db import transaction
from django.views import View


VIEW_LOG_TEMPLATE = "{view}\n{user}\n{method}\n{path}\n"
EXCEPTION_TEMPLATE = "{msg}\n{traceback}\n"

logger = logging.getLogger("exceptions")
view_logger = logging.getLogger("views.exceptions")


def logging(fn):
    """Logs exceptions."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as error:
            logger.error(
                fn.__name__
                + "\n"
                + EXCEPTION_TEMPLATE.format(
                    msg=str(error), traceback=traceback.format_exc()
                )
            )
            raise

    return wrapper


def logging_view(fn):
    """Logs views exceptions."""

    @functools.wraps(fn)
    def wrapper(request, *args, **kwargs):
        try:
            with transaction.atomic():
                return fn(request, *args, **kwargs)
        except Exception as error:
            view_logger.error(
                VIEW_LOG_TEMPLATE.format(
                    view=fn.__name__,
                    user=request.user,
                    method=request.method,
                    path=request.path,
                )
                + EXCEPTION_TEMPLATE.format(
                    msg=str(error), traceback=traceback.format_exc()
                )
            )
            raise

    return wrapper


class LoggingView(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                return super().dispatch(request, *args, **kwargs)
        except Exception as error:
            view_logger.error(
                VIEW_LOG_TEMPLATE.format(
                    view=self.__class__,
                    user=request.user,
                    method=request.method,
                    path=request.path,
                )
                + EXCEPTION_TEMPLATE.format(
                    msg=str(error), traceback=traceback.format_exc()
                )
            )
            raise
