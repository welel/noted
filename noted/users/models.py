from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _generate_username(self, full_name: str) -> str:
        """Generate username based on `full_name` field.

        Generate unique username for the database based on `full_name` field.

        Args:
            full_nmae: a full name of a user.
        Returns:
            The generated username.
        Raises:
            ValueError: if `full_name` is empty string or None.
        """
        if not full_name:
            raise ValueError("Full name is empty or None.")
        username = "@" + full_name.replace(" ", ".").lower()
        if not self.filter(username=username).exists():
            return username
        suffix = 2
        while self.filter(username=username + str(suffix)).exists():
            suffix += 1
        return username + str(suffix)

    def _create_user(
        self,
        email,
        password,
        **extra_fields,
    ):
        if not email:
            raise ValueError("Users must have an email address")
        now = timezone.now()
        email = self.normalize_email(email)
        username = extra_fields.get("username")
        if not username or self.filter(username=username).exists():
            full_name = extra_fields.get("full_name", "user")
            extra_fields["username"] = self._generate_username(full_name)
        user = self.model(
            email=email,
            is_active=True,
            date_joined=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        user = self._create_user(email, password, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """The main model for an account of a client.

    Fields:
        email: creation of a user happens after email authentication, so the
            `email` field is unique for users.
        full_name: store full name of a user.
        username: generates based on `first_name`.
    """

    email = models.EmailField(
        max_length=254, unique=True, blank=False, db_index=True, null=False
    )
    username = models.CharField(
        max_length=150, unique=True, blank=True, null=False
    )
    full_name = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self._state.adding and (
            not self.username
            or User.objects.filter(username=self.username).exists()
        ):
            full_name = self.full_name if self.full_name else "user"
            self.username = User.objects._generate_username(full_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} / {self.email}"

    def get_absolute_url(self):
        username = self.username.replace(".", "-")[1:]
        return f"/users/{username}/"


class SignupToken(models.Model):
    """A token used for authentication and sign up process.

    Created when sign up email was sent to a client. Deleted when a client
    registered on the website.
    """

    token = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
