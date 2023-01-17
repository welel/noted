from notifications.signals import notify

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from actions.models import Action
from users.models import UserProfile, User, Following


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


@receiver(post_save, sender=Following)
def following_created_action(sender, instance, created, **kwargs):
    if created:
        notify.send(
            instance.follower,
            verb="user_followed",
            recipient=instance.followed,
            description=_("started following you"),
        )
