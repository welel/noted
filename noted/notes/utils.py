from django.utils.text import slugify
from taggit.models import Tag, TaggedItem


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


def custom_tag_string(tag_string: str) -> list:
    """Tag string parser."""
    if not tag_string:
        return []
    if ',' not in tag_string and ' ' not in tag_string:
        return [tag_string]
    tags = []
    for i, tag in enumerate(tag_string.split(',')):
        tags.append(tag.strip().lower().replace(' ', '-'))
    return tags
