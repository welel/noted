"""Exceptions for the `users` application."""


class FirstNameDoesNotSetError(Exception):
    """Raised when the user doesn't have `first_name` or it's empty string."""

    def __init__(self, message="User dosen't have firt_name or it is empty."):
        self.message = message
        super().__init__(self.message)
