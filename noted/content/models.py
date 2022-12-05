"""
TODO: DRY - __str__, save, get_absolute_url
"""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from content.fields import MarkdownField, RenderedMarkdownField
from common import generate_unique_slug
from users.models import User


class Source(models.Model):
    DEFAULT = "0"
    BOOK = "1"
    COURSE = "2"
    VIDEO = "3"
    ARTICLE = "4"
    LECTURE = "5"
    TUTORIAL = "6"
    TYPES = (
        (DEFAULT, _("Other")),
        (BOOK, _("Book")),
        (COURSE, _("Course")),
        (VIDEO, _("Video")),
        (ARTICLE, _("Article")),
        (LECTURE, _("Lecture")),
        (TUTORIAL, _("Tutorial")),
    )
    title = models.CharField(
        max_length=200, blank=False, null=False, db_index=True
    )
    type = models.CharField(max_length=20, choices=TYPES, default=DEFAULT)
    slug = models.SlugField(max_length=254, unique=True, null=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, from_field="title")
        return super().save(*args, **kwargs)

    @classmethod
    def make_type_readable(cls, query):
        for type_code, type in cls.TYPES:
            if type_code == query:
                return type
        return None

    def get_readable_type(self):
        return Source.make_type_readable(self.type)

    # def get_absolute_url(self):
    #     return reverse("source", args=[self.slug])


class Note(models.Model):
    """Markdown text with a list of attributes.

    **Fields**
        title: a title of a note.
        slug: a slug of a note for URL.
        author: a user foreign key, author of a note.
        source: a link to a :model:`Source`.
        body_raw: a raw Markdown text from a form.
        body_html: HTML representation of `body_raw`, it is generated
                   based on `body_raw` via GitHub API.
        summary: a short summary on a text of a note.
        draft: a boolean flag makes a notes private (hides from other users).
        anonymous: a boolean flag hides an author of a note.
        pin: a boolean flag, gives functionality to pin notes.
        created: publish datetime of a note.
        modified: update datetime of a note.
        views: a counter of note's visitors.
        fork: a link to :model:`Note` if a note forked from another.
        allow_comments: a boolean flag allows to users leave comments
                        to a note.
        tags: tags of a note (max tags - 5, max length - 24 symbols).
        users_like: a m2m field for note likes.
        bookmarked: a m2m field for bookmarks for user.

    """

    title = models.CharField(
        max_length=100, null=False, blank=False, db_index=True
    )
    slug = models.SlugField(max_length=255, editable=False, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, editable=False
    )
    source = models.ForeignKey(
        Source,
        null=True,
        on_delete=models.SET_NULL,
        related_name="notes",
        blank=True,
    )
    body_raw = MarkdownField(rendered_field="body_html", blank=True)
    body_html = RenderedMarkdownField(max_length=70000, default="", blank=True)
    summary = models.CharField(
        max_length=250,
        default="",
        blank=True,
        help_text=_("Write summary on the note in 100 symbols."),
    )
    draft = models.BooleanField(
        default=False, help_text=_("Only you can see the note.")
    )
    anonymous = models.BooleanField(
        default=False, help_text=_("Others won't see that the note is yours.")
    )
    pin = models.BooleanField(
        default=False, help_text=_("The note will appear in pin notes list.")
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("content:note", args=[self.slug])
