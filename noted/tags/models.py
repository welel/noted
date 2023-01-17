from taggit.models import Tag, TaggedItem

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Count, QuerySet
from django.utils.text import slugify

from django.contrib.auth import get_user_model


class UnicodeTag(Tag):
    class Meta:
        proxy = True

    def slugify(self, tag, i=None):
        return slugify(self.name, allow_unicode=True)[:128]


class UnicodeTaggedItem(TaggedItem):
    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return UnicodeTag


def get_top_tags(top_num: int = 7) -> QuerySet:
    """Gets tags with most number of notes.

    Attrs:
        top_num: a slice size from the top.
    """
    return (
        Tag.objects.annotate(
            num_times=Count("notes", filter=Q(notes__draft=False))
        )
        .filter(num_times__gt=0)
        .order_by("-num_times")[:top_num]
    )


def get_tag_followers(tag: Tag) -> list:
    ctype = ContentType.objects.get(model="userprofile")
    items = UnicodeTaggedItem.objects.filter(tag=tag, content_type=ctype)
    return list([item.content_object.user for item in items])
