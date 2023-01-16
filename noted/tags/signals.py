from notifications.signals import notify

from django.db.models.signals import post_save
from django.dispatch import receiver

from tags.models import UnicodeTaggedItem


# @receiver(post_save, sender=UnicodeTaggedItem)
# def tagged_note_created_action(sender, instance, created, **kwargs):
#     """Create an action (:model:`Action`) if a note instance was created."""
#     if created:
#         notify.send(
#             instance.content_object,
#             verb="tagged_note_created",
#             recipient=instance.tag.users.all(),
#             target=instance.tag,
#             description='Created new note "{}" with the tag - {}.'.format(
#                 instance.content_object.title, instance.tag.name
#             ),
#         )
