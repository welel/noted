import logging
import traceback

from django.core.cache import cache
from django.db.models import Count
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

import pycld2 as cld2
from taggit.models import Tag

from actions import base as act
from actions.models import Action
from common.logging import EXCEPTION_TEMPLATE

from .models import Note


logger = logging.getLogger("exceptions")


@receiver(post_delete, sender=Note)
def free_source(sender, instance, **kwargs):
    """Delete :model:`Source` instance from the database if it has 0 notes."""
    if instance.source and not instance.source.notes.all():
        instance.source.delete()


@receiver(post_delete, sender=Note)
def free_tags(sender, instance, **kwargs):
    """Delete unused tags from the database (if it has 0 notes)."""
    Tag.objects.annotate(ntag=Count("taggit_taggeditem_items")).filter(
        ntag=0
    ).delete()


@receiver(pre_save, sender=Note)
def set_lang(sender, instance, **kwargs):
    """Detect languange of note text and set to `lang`."""
    is_reliable = False
    try:
        is_reliable, _, details = cld2.detect(instance.body_raw)
    except Exception as error:
        logger.error(
            "An error occured while detecting the language."
            + EXCEPTION_TEMPLATE.format(
                name=set_lang.__name__,
                msg=str(error),
                args=str(instance.pk),
                kwargs=str(kwargs),
                traceback=traceback.format_exc(),
            )
        )
    lang_code = details[0][1]
    if is_reliable and lang_code in (Note.RU, Note.EN):
        instance.lang = lang_code
    else:
        instance.lang = Note.ER
        logger.warning(
            f"Language is not detected ({lang_code}\nNote body:{instance.body_raw}"
        )


@receiver(post_save, sender=Note)
def note_created_actions(sender, instance, created, **kwargs):
    """Create actions if a note instance was created."""
    if created:
        Action.objects.create_action(
            instance.author, act.CREATE, target=instance, notify=True
        )


# @receiver(post_save, sender=Note)
# def free_cache(sender, instance, created, **kwargs):
#     """Create actions if a note instance was created."""
#     cache.delete_pattern("*PublicNoteList*")
