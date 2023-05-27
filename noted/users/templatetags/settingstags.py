from typing import Literal

from django import template
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from ..base import UITheme


register = template.Library()


@register.filter
def theme(user_theme: Literal[UITheme.DARK, UITheme.LIGHT]) -> str:
    if user_theme == UITheme.DARK:
        theme_path = settings.DARK_THEME_PATH
    else:
        theme_path = settings.LIGHT_THEME_PATH
    return "{}{}".format(settings.STATIC_URL, theme_path)


@register.filter
def print_theme(user_theme: Literal[UITheme.DARK, UITheme.LIGHT]) -> str:
    """Returns a label for the theme toggler."""
    if user_theme == UITheme.DARK:
        return _("Light theme")
    return _("Dark theme")
