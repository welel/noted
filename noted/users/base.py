from enum import Enum


class UITheme(str, Enum):
    LIGHT = "light"
    DARK = "dark"


class TokenType(str, Enum):
    SIGNUP = "sn"
    CHANGE_EMAIL = "cm"


def user_avatars_path(instance, filename):
    """Return a path to a user's profile picture."""
    return f"user/avatars/{instance.id}/{filename}"


def default_social_media_json():
    return {"facebook": "", "twitter": "", "github": ""}


def default_profile_settings():
    return {"theme": UITheme.LIGHT}
