import json
from typing import Literal

from taggit.managers import TaggableManager

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.text import is_latin, transcript_ru2en
from tags.models import UnicodeTaggedItem

from .validators import validate_image


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


def user_avatars_path(instance, filename):
    """Return a path to a user's profile picture."""
    return f"user/avatars/{instance.id}/{filename}"


def default_social_media_json():
    return {"facebook": "", "twitter": "", "github": ""}


class User(AbstractBaseUser, PermissionsMixin):
    """The main model for an account of a client.

    Fields:
        email: Creation of a user happens after email authentication, so the
            `email` field is unique for users.
        full_name: Store full name of a user.
        username: Generates based on `first_name`.
        ...
    """

    email = models.EmailField(
        _("Email"),
        max_length=254,
        unique=True,
        blank=False,
        db_index=True,
        null=False,
    )
    username = models.CharField(
        _("Username"),
        max_length=150,
        unique=True,
        blank=True,
        null=False,
        help_text=_(
            "Username should include only latin letters, digits and dots. \
            Username can't start and end with a dot or don't contain letters. \
            Digits can be added only at the end."
        ),
    )
    full_name = models.CharField(
        _("Full Name"),
        max_length=50,
        blank=True,
        help_text=_(
            "Your name appear around NoteD where you post or do actions."
        ),
    )
    is_staff = models.BooleanField(_("Staff"), default=False)
    is_superuser = models.BooleanField(_("Superuser"), default=False)
    is_active = models.BooleanField(_("User activated"), default=True)
    last_login = models.DateTimeField(_("Last Login"), null=True, blank=True)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)

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
        return f"{self.username}"

    @classmethod
    def unslugify(cls, slug: str) -> str:
        """Returns `username` for slug."""
        return "@" + slug.replace("-", ".")

    @property
    def slug(self) -> str:
        return self.username[1:].replace(".", "-")

    def get_absolute_url(self):
        return reverse("content:profile_notes", args=[self.slug])

    @property
    def given_name(self) -> str:
        name = self.full_name.split()
        if len(name) == 2:
            return name[0]
        return name

    @property
    def family_name(self) -> str:
        name = self.full_name.split()
        if len(name) == 2:
            return name[1]
        return name


def default_profile_settings():
    return {"theme": "ligth",}


class UserProfile(models.Model):
    """Additional fields for the :models:`User` model.

    Fields:
        location: Simple text to indicate user's location (country, city, etc.)
            at the discretion of the user.
        socials: JSON with links to user's social media ({"social_name":"link"})
        settings: JSON with profile+user settings.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("Profile"),
    )
    avatar = models.ImageField(
        _("Profile picture"),
        upload_to=user_avatars_path,
        default=settings.DEFAULT_USER_AVATAR_PATH,
        validators=[validate_image],
    )
    bio = models.TextField(_("Bio"), max_length=700, blank=True)
    location = models.CharField(_("Location"), max_length=40, blank=True)
    socials = models.JSONField(
        _("Social Media Links"), blank=True, default=default_social_media_json
    )
    settings = models.JSONField(
        _("Settings"), blank=True, default=default_profile_settings
    )
    tags = TaggableManager(
        through=UnicodeTaggedItem,
        blank=True,
        related_name="users",
        verbose_name=_("Tag subscriptions"),
    )

    def __str__(self):
        return f"Profile: {self.user.username}"

    def get_socials(self) -> dict:
        """Gets a dict with social media usernames.

        Structure:
            {"name of social name": "username"}
        """
        if isinstance(self.socials, str):
            return json.loads(self.socials)
        return self.socials

    @property
    def twitter(self) -> str:
        """Returns twitter username."""
        return self.get_socials()["twitter"]

    @property
    def facebook(self) -> str:
        """Returns facebook username."""
        return self.get_socials()["facebook"]

    @property
    def github(self) -> str:
        """Returns github username."""
        return self.get_socials()["github"]

    @property
    def is_socials(self) -> bool:
        """Checks does an user have social media."""
        return self.twitter or self.facebook or self.github
    
    def set_theme(self, theme: Literal["ligth", "dark"]):
        if theme not in ("ligth", "dark"):
            raise KeyError("Available themes: light, dark.")
        self.settings["theme"] = theme


class FollowingManager(models.Manager):
    def get_following(self, user: User) -> list:
        """Return list of users that follow a required user.

        Args:
            user: A required user.
        """
        return [following.followed for following in self.filter(follower=user)]

    def get_follower(self, user: User) -> list:
        """

        Args:
            user: A required user.
        """
        return [following.follower for following in self.filter(followed=user)]


class Following(models.Model):
    follower = models.ForeignKey(
        User,
        related_name="subscriptions",
        db_index=True,
        on_delete=models.CASCADE,
    )
    followed = models.ForeignKey(
        User, related_name="followers", db_index=True, on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    objects = FollowingManager()

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.follower} follows {self.followed}"


class AuthToken(models.Model):
    """A token used for authentication, sign up and change email process.

    Created when sign_up/change_email email was sent to a client.
    Deleted when a client has done a process.

    """

    SIGNUP = "sn"
    CHANGE_EMAIL = "cm"
    TYPES = (
        (SIGNUP, _("Sign Up Token")),
        (CHANGE_EMAIL, _("Change Email Token")),
    )
    token = models.CharField(_("Token"), max_length=255, unique=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    type = models.CharField(_("Type"), max_length=2, choices=TYPES)

    def __str__(self):
        return "{token} ({type})".format(token=self.token, type=self.type)

    @classmethod
    def get_from_str(
        cls, token: str, type: Literal["sn", "cm"]
    ) -> "AuthToken":
        """Gets a token from database by the token string and the type."""
        return cls.objects.get(token=token, type=type)
