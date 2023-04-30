from typing import Literal

from django import template
from django.conf import settings
from django.utils.translation import get_language

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

    # TODO: solve problem with gettext/gettext_lazy, any of this functions is
    # not working in this filter.

    THEME = {
        "ru": {UITheme.DARK: "Тёмная тема", UITheme.LIGHT: "Светлая тема"},
        "en": {UITheme.DARK: "Dark theme", UITheme.LIGHT: "Light theme"},
    }

    lang_code = get_language()

    if user_theme == UITheme.DARK:
        return THEME[lang_code][UITheme.LIGHT]
    return THEME[lang_code][UITheme.DARK]
