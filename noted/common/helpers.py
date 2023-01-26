from django.contrib.sites.models import Site
from django.conf import settings


def get_absolute_uri(path: str):
    return "{schema}://{domain}{path}".format(
        schema=settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL,
        domain=Site.objects.get_current().domain,
        path=path,
    )
