from django import template
from django.conf import settings


register = template.Library()


@register.filter
def full_url(path: str) -> str:
    """Translates a path to the full URL to the document.

    Example:
        `/about` -> `http://welel-noted.site/about`
    """

    return "{}://{}{}".format(
        settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL, settings.ALLOWED_HOSTS[0], path
    )


@register.filter
def min_required(min: str) -> str:
    """Returns the time required CEO tag for `schemas.org` for input minutes."""
    return f"PT{min}M"
