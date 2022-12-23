import functools
import logging

logger = logging.getLogger(__name__)


def logging(fn):
    """Logs exceptions."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as error:
            logger.error(error)
            raise


def logging_view(fn):
    """Logs exceptions."""

    @functools.wraps(fn)
    def wrapper(request, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as error:
            logger.error(error)
            raise
