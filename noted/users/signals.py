from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from actions import base as act
from actions.models import Action

from .models import Following, User, UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a user profile for a user."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def user_created_action(sender, instance, created, **kwargs):
    """Create an action (:model:`Action`) if a user was created."""
    if created:
        Action.objects.create_action(instance, act.NEW)


@receiver(post_save, sender=Following)
def following_created_action(sender, instance, created, **kwargs):
    if created:
        Action.objects.create_action(
            instance.follower, act.FOLLOW, instance.followed, notify=True
        )
