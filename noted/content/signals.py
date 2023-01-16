import logging
import traceback

import pycld2 as cld2
from taggit.models import Tag
from notifications.signals import notify

from django.db.models import Count
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from actions.models import Action
from content.models import Note
from common.logging import EXCEPTION_TEMPLATE
from users.models import Following


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
def note_created_action(sender, instance, created, **kwargs):
    """Create an action (:model:`Action`) if a note instance was created."""
    if created:
        Action.objects.create_action(
            instance.author, Action.NEW_NOTE, target=instance
        )
        notify.send(
            instance.author,
            recipient=Following.objects.get_follower(instance.author),
            verb="note_created",
            target=instance,
            description=_("created new note"),
        )
