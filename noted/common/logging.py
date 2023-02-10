"""Loggining system for general, views and generic functions."""

import functools
import logging
import traceback
from typing import Callable, Dict, Type

from django.db import transaction
from django.http import HttpRequest
from django.views import View
from django.views.generic.base import View


request_logger = logging.getLogger("django.request")


class LogMessage:
    def __init__(
        self,
        error: Type[Exception],
        func: Callable,
        *args,
        class_view: Type[View] = None,
        request: Type[HttpRequest] = None,
        **kwargs,
    ):
        self.error = error
        self.function = func
        self.request = request
        self.class_view = class_view
        self.args = args
        self.kwargs = kwargs

    def __str__(self) -> str:
        message = []

        if self.class_view:
            message.append(f"Class view name: {self.class_view.__class__}\n")

        if self.request:
            message.append(f"Request: {repr(self.request)}\n")

        message.append(
            "Function name: {func_name}\nError message: {error_message}\n"
            "Args: {args}\nKwargs: {kwargs}\nTraceback: \n{traceback}\n".format(
                func_name=self.function.__name__,
                error_message=str(self.error),
                args=str(self.args),
                kwargs=str(self.kwargs),
                traceback=traceback.format_exc(),
            )
        )
        return "".join(message)


class LoggerDecorator:
    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                log_message = self.get_log_message(
                    error, func, *args, **kwargs
                )
                self.logger.error(log_message)
                raise

        return wrapper

    def get_log_message(
        self, error: Exception, func: Callable, *args, **kwargs
    ) -> str:
        # If Class Based View
        if (
            len(args) >= 2
            and issubclass(type(args[0]), View)
            and issubclass(type(args[1]), HttpRequest)
        ):
            return str(
                LogMessage(
                    error,
                    func,
                    *args,
                    class_view=args[0],
                    request=args[1],
                    **kwargs,
                )
            )
        # If Function Based View
        elif len(args) >= 1 and isinstance(args[0], HttpRequest):
            return str(
                LogMessage(error, func, *args, request=args[0], **kwargs)
            )
        else:
            return str(
                LogMessage(error, func, *args, request=args[0], **kwargs)
            )
