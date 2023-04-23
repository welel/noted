from django.contrib.auth.models import BaseUserManager

from django.db import models
from django.utils import timezone

from common.text import is_latin, transcript_ru2en


class UserManager(BaseUserManager):
    def _generate_username(self, full_name: str) -> str:
        """Generate username based on `full_name` field.

        Generate unique username for the database based on `full_name` field.

        Args:
            full_nmae: A full name of a user.

        Returns:
            The generated username.

        Raises:
            ValueError: if `full_name` is empty string or None.
        """
        if not full_name:
            raise ValueError("Full name is empty or None.")
        if not is_latin(full_name.replace(" ", "")):
            full_name = transcript_ru2en(full_name)
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


class FollowingManager(models.Manager):
    def get_following(self, user: "User") -> list:
        """Return list of users that follow a required user.

        Args:
            user: A required user.
        """
        return [following.followed for following in self.filter(follower=user)]

    def get_follower(self, user: "User") -> list:
        """

        Args:
            user: A required user.
        """
        return [following.follower for following in self.filter(followed=user)]
