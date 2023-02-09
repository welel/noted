import unicodedata as ud
import uuid

from django.core.exceptions import FieldDoesNotExist
from django.utils.text import slugify


def transcript_ru2en(text: str) -> str:
    """Makes phonetic transcription of Russian text to English.

    Args:
        text: The Russian text to be translated.

    Returns:
        The translated text in English.

    Example:
    >>> transcript_ru2en("Привет, миръ!")
    "Privet, mir!"
    """
    trans_dict = str.maketrans(
        "абвгдеёжзийклмнопрстуфхцчшщыэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ",
        "abvgdeejziiklmnoprstufhcchhieuaABVGDEEJZIIKLMNOPRSTUFHCCHHIEUA",
        "ъьЪЬ",
    )
    return text.translate(trans_dict)


def generate_unique_slug(
    instance,
    from_field: str = "title",
    for_field: str = "slug",
    latin: bool = False,
) -> str:
    """Generate unique slug for model based on another field.

    The method slugifys value of one field and adds random symbols
    at the end if slug isn't unique for the databse.

    Args:
        instance: A model instance.
        from_field: The name of a field where take a the value for generating.
        for_field: A name of slug field, for the uniqueness check.
        latin: If True translates Russian letters to Latin.

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

    if latin:
        from_field_val = transcript_ru2en(from_field_val)

    slug = slugify(from_field_val, allow_unicode=True)[:245]
    if model.objects.filter(**{for_field: slug}).exists() or not slug:
        return slug + "-" + str(uuid.uuid1())[:8]
    return slug


def is_latin(word: str) -> bool:
    """Checks if a word is written in Latin script.

    Args:
        word: The word to check.

    Returns:
        True if the word is written in Latin script, False otherwise.
    """
    return all(["LATIN" in ud.name(char, "") for char in word])
