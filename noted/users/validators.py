import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_image(image):
    limit_kb = 512
    if image.file.size > limit_kb * 1024:
        raise ValidationError(_(f"Max size of file is {limit_kb} KB."))

    if image.height > 512 or image.width > 512:
        raise ValidationError(_(f"Max size of file is 250x250 px."))


def validate_username(username: str):
    """Validates username.

    Min length = 5
    Max length = 150
    Username starts with '@' sign.
    """
    if 5 > len(username) or len(username) > 150:
        raise ValidationError(
            _(
                f"Username should contain less than 150 symbols \
                    and more than 4."
            )
        )
    if username[0] != "@":
        raise ValidationError(_("Username should start with '@' sign."))
    if not re.fullmatch(
        r"^@([a-zA-Z]+\.[a-zA-Z]+\.?)+[a-zA-Z]+\d*$", username
    ):
        raise ValidationError(
            _(
                "Username can't start or end with a dot. Two dots can't be \
                next to each other. Digits can be added only at the end."
            )
        )


def validate_full_name(full_name: str):
    """Validates full name."""
    if not full_name:
        raise ValidationError(_("Full name can't be empty."))
    if not full_name.replace(" ", "").isalpha():
        raise ValidationError(_("Full name should contain only letters."))
    if len(full_name.split()) > 3:
        raise ValidationError(_("Full name should contain less than 3 words."))


def validate_social_username(username: str):
    """Validates full name."""
    if "?" in username:
        raise ValidationError(_("Username should not contain '?' sign."))
    if len(username) > 200:
        raise ValidationError(
            _("Username should contain less than 200 symbols.")
        )
