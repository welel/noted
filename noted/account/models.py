from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """The main model for an account of a client.

    Fields:
        email: creation of a user happens after email authentication, so the
            `email` field is unique for users.
        first_name: store full name of a user.
        username: generates based on `first_name`.
    """

    email = models.EmailField(_("Email address"), unique=True, blank=False)

    def __str__(self):
        return f"{self.username} / {self.email}"


class SignupToken(models.Model):
    """A token used for authentication and sign up process.

    Created when sign up email was sent to a client. Deleted when a client
    registered on the website.
    """

    token = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
