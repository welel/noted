from taggit.models import Tag

from django.db.models import Count
from django.db.models.signals import post_delete
from django.dispatch import receiver

from content.models import Note


@receiver(post_delete, sender=Note)
def free_source(sender, instance, **kwargs):
    """Delete :model:`Source` instance from the database if it has 0 notes."""
    if instance.source and not instance.source.notes.all():
        instance.source.delete()


@receiver(post_delete, sender=Note)
def free_tags(sender, instance, **kwargs):
    """
    Delete unused tags from the database (if it has 0 notes).
    """
    Tag.objects.annotate(ntag=Count("taggit_taggeditem_items")).filter(
        ntag=0
    ).delete()
