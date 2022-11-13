from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from actions.models import Action
from actions.utils import create_action
from notes.models import Note, Comment


@receiver(post_save, sender=Note)
def create_note_created_action(sender, instance, created, **kwargs):
    """Create an action (:model:`Action`) if a note instance was created."""
    if created:
        create_action(instance.author, Action.NEW_NOTE, target=instance)


@receiver(post_save, sender=Comment)
def create_comment_created_action(sender, instance, created, **kwargs):
    """Create an action (:model:`Action`) if a comment instance was created."""
    if created:
        create_action(instance.author, Action.NEW_COMMENT, target=instance)
