import uuid

from django.core.exceptions import FieldError
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

from taggit.managers import TaggableManager

from markdown.fields import MarkdownField, RenderedMarkdownField
from tags.models import UnicodeTaggedItem
from user.models import User


class NoteManager(models.Manager):

    def get_personal_notes(self, user):
        return self.filter(author=user)


class Note(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(max_length=255, editable=False, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, editable=False
    )
    source = models.URLField(
        blank=True, default='',
        help_text='Place a link to the source to which you are taking notes.'
    )
    body_raw = MarkdownField(rendered_field='body_html')
    body_html = RenderedMarkdownField(max_length=40000, default='', blank=True)
    summary = models.CharField(
        max_length=100, default='', blank=True,
        help_text='Write summary on the note in 100 symbols.'
    )
    private = models.BooleanField(
        default=False, help_text='Only you can see the note.'
    )
    anonymous = models.BooleanField(
        default=False, help_text='Others won\'t see that the note is yours.'
    )
    date = models.DateTimeField(auto_now=True)
    tags = TaggableManager(
        through=UnicodeTaggedItem, blank=True,
        help_text='''Add tags. Separate tags by using "Enter" or comma.
        You can add maximum 5 tags, and length of tags should be less than 25
        symbols.'''
    )
    objects = NoteManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self._generate_unique_slug()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('note', args=[self.slug, ])

    def _generate_unique_slug(self) -> str:
        """Generates unique slug for ``Note`` instance.

        The method slugifys `title` and adds random symbols
        at the end if `slug` isn't unique.

        """
        if not self.title:
            raise FieldError(
                'Cannot generate `slug`, because `title` is empty.'
            )
        slug = slugify(self.title, allow_unicode=True)
        if Note.objects.filter(slug=slug).exists():
            slug += str(uuid.uuid1())[:8]
        return slug[:255]
