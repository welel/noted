import re

from PIL import Image

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_image(image: Image) -> None:
    """Checks if the image size is within the allowed limit.

    Args:
        image: The image file to validate.

    Raises:
        ValidationError: If the size of the image file is larger than
            the allowed limit.
    """
    limit_kb = 512
    if image.file.size > limit_kb * 1024:
        raise ValidationError(_(f"Max size of file is {limit_kb} KB."))


def validate_username(username: str) -> None:
    """Validates a given username.

    Args:
        username: The username to validate.

    Raises:
        ValidationError: If the username is not a str, doesn't meet
            the length requirements, doesn't start with '@' or is not in
            the correct format.
    """
    if not isinstance(username, str):
        raise ValidationError(_("Bad username type."))
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


def validate_full_name(full_name: str) -> None:
    """Validates a given full name.

    Args:
        full_name: The full name to validate.

    Raises:
        ValidationError: If the full name is empty, contains non-alphabetic
            characters, or has more than three words.
    """
    if not full_name:
        raise ValidationError(_("Full name can't be empty."))
    if not full_name.replace(" ", "").isalpha():
        raise ValidationError(_("Full name should contain only letters."))
    if len(full_name.split()) > 3:
        raise ValidationError(_("Full name should contain less than 3 words."))


def validate_social_username(username: str) -> None:
    """Validates a given social media username.

    Args:
        username: The username to validate.

    Raises:
        ValidationError: If the username contains the '?' character or
            is longer than 200 characters.
    """
    if "?" in username:
        raise ValidationError(_("Username should not contain '?' sign."))
    if len(username) > 200:
        raise ValidationError(
            _("Username should contain less than 200 symbols.")
        )
