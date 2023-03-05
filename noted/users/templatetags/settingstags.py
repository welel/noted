from typing import Literal

from django import template
from django.conf import settings


register = template.Library()


@register.filter
def theme(user_theme: Literal["ligth", "dark"]) -> str:
    if user_theme == "dark":
        theme_path = settings.DARK_THEME_PATH
    else:
        theme_path = settings.LIGTH_THEME_PATH
    return "{}{}".format(settings.STATIC_URL, theme_path)
