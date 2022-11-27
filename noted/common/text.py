import uuid

from django.core.exceptions import FieldDoesNotExist
from django.utils.text import slugify


def generate_unique_slug(instance) -> str:
    """Generate unique `slug` for model based on `title`.

    The method slugifys `title` and adds random symbols
    at the end if `slug` isn't unique for the databse.

    Args:
        instance: a model instance.
    Returns:
        A generated unique slug.
    """
    model = type(instance)
    try:
        model._meta.get_field("title")
    except:
        FieldDoesNotExist("Model must have `title` field.")
    try:
        model._meta.get_field("slug")
    except:
        FieldDoesNotExist("Model must have `slug` field.")

    if not instance.title:
        raise ValueError("Cannot generate `slug`, because `title` is empty.")
    slug = slugify(instance.title, allow_unicode=True)[:245]
    if model.objects.filter(slug=slug).exists():
        return slug + "-" + str(uuid.uuid1())[:8]
    return slug
