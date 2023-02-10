import uuid

from taggit.models import Tag, TaggedItem

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Count, Q, QuerySet
from django.utils.text import slugify

from common.text import transcript_ru2en


class TagManager(models.Manager):
    def _generate_unique_slug(self, object) -> str:
        """Generates a unique slug based on an object name."""
        name = transcript_ru2en(object.name)
        slug = slugify(name, allow_unicode=True)[:128]
        if self.filter(slug=slug).exists():
            slug += str(uuid.uuid4())[:8]
        return slug


class UnicodeTag(Tag):
    objects = TagManager()

    class Meta:
        proxy = True

    def slugify(self, *args):
        return UnicodeTag.objects._generate_unique_slug(self)


class UnicodeTaggedItem(TaggedItem):
    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return UnicodeTag


def get_top_tags(top_num: int = 7) -> QuerySet:
    """Gets tags with most number of notes.

    TODO: Try to put it in a Manager.

    Attrs:
        top_num: a slice size from the top.
    """
    return (
        UnicodeTag.objects.annotate(
            num_times=Count("notes", filter=Q(notes__draft=False))
        )
        .filter(num_times__gt=0)
        .order_by("-num_times")[:top_num]
    )


def get_tag_followers(tag: Tag) -> list:
    """Gets a list of users who follow the given tag

    Args:
        tag: A Tag object.

    Returns:
        A list of users who follow the given tag.
    """
    profile_ct = ContentType.objects.get(model="userprofile")
    items = UnicodeTaggedItem.objects.filter(tag=tag, content_type=profile_ct)
    return list([item.content_object.user for item in items])
