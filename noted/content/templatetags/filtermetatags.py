from django import template
from django.utils.safestring import mark_safe
from django.conf import settings


register = template.Library()


@register.filter
def full_url(path: str) -> str:

    return "{}://{}{}".format(
        settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL, settings.ALLOWED_HOSTS[0], path
    )


@register.filter
def min_required(min: str) -> str:
    return f"PT{min}M"
