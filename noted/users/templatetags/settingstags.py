from typing import Literal

from django import template
from django.conf import settings
from django.utils.translation import gettext as _


register = template.Library()


@register.filter
def theme(user_theme: Literal["ligth", "dark"]) -> str:
    if user_theme == "dark":
        theme_path = settings.DARK_THEME_PATH
    else:
        theme_path = settings.LIGTH_THEME_PATH
    return "{}{}".format(settings.STATIC_URL, theme_path)


@register.filter
def print_theme(user_theme: Literal["ligth", "dark"]) -> str:
    """Returns a label for the theme toggler."""
    if user_theme == "dark":
        return _("Light theme")
    return _("Dark theme")
