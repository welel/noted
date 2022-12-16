from django.db.models.signals import post_delete
from django.dispatch import receiver

from content.models import Note


@receiver(post_delete, sender=Note)
def free_source(sender, instance, **kwargs):
    """Delete :model:`Source` instance from the database if it has 0 notes."""
    if instance.source and not instance.source.notes.all():
        instance.source.delete()
