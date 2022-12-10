import uuid

from django.core.exceptions import FieldDoesNotExist
from django.utils.text import slugify


def generate_unique_slug(
    instance, from_field: str = "title", for_field: str = "slug"
) -> str:
    """Generate unique slug for model based on another field.

    The method slugifys value of one field and adds random symbols
    at the end if slug isn't unique for the databse.

    Args:
        instance: a model instance.
        from_field: the name of a field where take a the value for generating.
        for_field: a name of slug field, for the uniqueness check.
    Returns:
        A generated unique slug.
    """
    model = type(instance)
    try:
        model._meta.get_field(from_field)
    except FieldDoesNotExist:
        raise FieldDoesNotExist(f"Model must have `{from_field}` field.")
    try:
        model._meta.get_field(for_field)
    except FieldDoesNotExist:
        raise FieldDoesNotExist(f"Model must have slug field - `{for_field}`.")

    from_field_val = getattr(instance, from_field)
    if not from_field_val:
        raise ValueError(
            f"Cannot generate `slug`, because `{from_field}` is empty."
        )
    slug = slugify(from_field_val, allow_unicode=True)[:245]
    if model.objects.filter(**{for_field: slug}).exists():
        return slug + "-" + str(uuid.uuid1())[:8]
    return slug
