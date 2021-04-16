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
