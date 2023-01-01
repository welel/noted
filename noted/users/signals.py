from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import UserProfile, User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a user profile for a user."""
    if created:
        UserProfile.objects.create(user=instance)
