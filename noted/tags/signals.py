from notifications.signals import notify

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from content.models import Note
from tags.models import UnicodeTaggedItem, get_tag_followers


@receiver(post_save, sender=UnicodeTaggedItem)
def tagged_note_created_action(sender, instance, created, **kwargs):
    """Create an action (:model:`Action`) if a tagged note was created."""
    if created and isinstance(instance.content_object, Note):
        notify.send(
            instance.tag,
            verb="tagged_note_created",
            recipient=get_tag_followers(instance.tag),
            target=instance.content_object,
            description=_("created new note with the tag that you follow"),
        )
