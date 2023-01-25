from django.db.models.signals import post_save
from django.dispatch import receiver

from actions import base as act
from actions.notifications import create_notification
from content.models import Note

from .models import UnicodeTaggedItem


@receiver(post_save, sender=UnicodeTaggedItem)
def tagged_note_created_action(sender, instance, created, **kwargs):
    """Create an action (:model:`Action`) if a tagged note was created."""
    if created and isinstance(instance.content_object, Note):
        create_notification(instance.tag, act.CREATE, instance.content_object)
