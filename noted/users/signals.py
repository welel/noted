from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from actions.models import Action
from content.models import Note
from users.models import UserProfile, User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a user profile for a user."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def user_created_action(sender, instance, created, **kwargs):
    """Create an action (:model:`Action`) if a user was created."""
    if created:
        Action.objects.create_action(instance, Action.NEW_USER)
