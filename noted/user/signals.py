from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from actions.models import Action
from actions.utils import create_action
from notes.models import Note
from user.models import Profile


User = get_user_model()

@receiver(pre_delete, sender=User)
def make_notes_anonymous(sender, instance, **kwargs):
    """Makes notes without an author anonymous.
    
    If a user is going to be deleted, makes his notes anonymous.
    """
    notes = Note.objects.filter(author=instance)
    for note in notes:
        note.anonymous = True
        note.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a user profile for a user."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_created_action(sender, instance, created, **kwargs):
    """Create an action (:model:`Action`) if a user was created."""
    if created:
        create_action(instance, Action.NEW_USER)
