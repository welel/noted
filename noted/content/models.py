from datetime import date
import io
from typing import Optional

from bs4 import BeautifulSoup
from taggit.managers import TaggableManager
import pdfkit

from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    TrigramSimilarity,
    SearchHeadline,
)
from django.db import models
from django.db.models import QuerySet, Count, Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from content.fields import MarkdownField, RenderedMarkdownField
from common import generate_unique_slug
from tags.models import UnicodeTaggedItem
from users.models import User


class SourceManager(models.Manager):
    def by_type(self, type_code: str) -> QuerySet:
        return self.filter(type=type_code)

    def search(self, query: str) -> QuerySet:
        similarity = TrigramSimilarity("title", query)
        return (
            self.annotate(similarity=similarity)
            .filter(similarity__gte=0.1)
            .order_by("-similarity")
        )


class Source(models.Model):
    """An information source.

    Links to a note(s).

    """

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
    type = models.CharField(
        _("Type"), max_length=20, choices=TYPES, default=DEFAULT
    )
    title = models.CharField(
        _("Title"), max_length=200, blank=False, null=False, db_index=True
    )
    link = models.URLField(
        _("Link to the source"), max_length=255, blank=True, default=""
    )
    description = models.CharField(
        _("Description"), max_length=100, blank=True, default=""
    )
    slug = models.SlugField(_("Slug"), max_length=254, unique=True, null=False)
    objects = SourceManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        return super().save(*args, **kwargs)

    @classmethod
    def make_type_readable(cls, type_code: str) -> Optional[str]:
        """Translate a source type code to a readable type name."""
        for code, name in cls.TYPES:
            if code == type_code:
                return name
        return None

    def get_readable_type(self) -> Optional[str]:
        """Return readable source type name."""
        return Source.make_type_readable(self.type)

    def get_absolute_url(self):
        return reverse("content:source", args=[self.slug])


class NoteManager(models.Manager):
    def personal(self, user: User) -> QuerySet:
        """Query notes for a specific user.

        Args:
            user: an author of notes.
        Returns:
            Notes for a specific user.
        """
        return self.filter(author=user)

    def public(self) -> QuerySet:
        """Query notes available for everyone."""
        return self.filter(draft=False)

    def datetime_created(self) -> QuerySet:
        return self.order_by("created")

    def datetime_created_dec(self) -> QuerySet:
        return self.order_by("-created")

    def by_source_type(self, type_code: str) -> QuerySet:
        return self.filter(draft=False, source__type=type_code)

    def popular(self) -> QuerySet:
        return self.filter(draft=False).order_by("-views")

    def most_liked(self) -> QuerySet:
        """Query notes sorted by number of likes from the most to least."""
        return (
            self.filter(draft=False)
            .annotate(count=Count("likes"))
            .order_by("-count")
        )

    def tags_notes(self, tag_names: list) -> QuerySet:
        return self.filter(draft=False, tags__name__in=tag_names).distinct()

    def search(self, query: str) -> QuerySet:
        search_vector = (
            SearchVector("title", weight="A")
            + SearchVector("summary", weight="A")
            + SearchVector("body_raw", weight="B")
        )
        search_query = SearchQuery(query)
        headline = SearchHeadline(
            "title", search_query, start_sel="<mark>", stop_sel="</mark>"
        )
        return (
            self.filter(draft=False)
            .annotate(
                rank=SearchRank(search_vector, search_query),
                similarity=TrigramSimilarity("title", query),
                headline=headline,
            )
            .filter(Q(rank__gte=0.2) | Q(similarity__gt=0.1))
            .order_by("-rank")
        )


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
        likes: a m2m field for note likes.
        bookmarked: a m2m field for bookmarks for user.
        tags: tags of a note (max tags - 3, max length - 24 symbols).
        *allow_comments: a boolean flag allows to users leave comments
                        to a note.

    """

    title = models.CharField(
        _("Title"), max_length=100, null=False, blank=False, db_index=True
    )
    slug = models.SlugField(
        _("Slug"), max_length=255, editable=False, unique=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        verbose_name=_("Author"),
    )
    source = models.ForeignKey(
        Source,
        null=True,
        on_delete=models.SET_NULL,
        related_name="notes",
        blank=True,
        verbose_name=_("Source"),
    )
    body_raw = MarkdownField(
        _("Markdown body"), rendered_field="body_html", blank=True
    )
    body_html = RenderedMarkdownField(
        _("HTML body"), max_length=70000, default="", blank=True
    )
    summary = models.CharField(
        _("Summary"),
        max_length=250,
        default="",
        blank=True,
        help_text=_("Write summary on the note in 100 symbols."),
    )
    draft = models.BooleanField(
        _("Draft"), default=False, help_text=_("Only you can see the note.")
    )
    anonymous = models.BooleanField(
        _("Anonymous"),
        default=False,
        help_text=_("Others won't see that the note is yours."),
    )
    pin = models.BooleanField(
        _("Pin"),
        default=False,
        help_text=_("The note will appear in pin notes list."),
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)
    views = models.PositiveIntegerField(_("Views"), default=0)
    fork = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Parent"),
        blank=True,
    )
    likes = models.ManyToManyField(
        User, related_name="liked_notes", blank=True
    )
    bookmarks = models.ManyToManyField(
        User, related_name="bookmarked_notes", default=None, blank=True
    )
    tags = TaggableManager(
        through=UnicodeTaggedItem,
        blank=True,
        related_name="notes",
        help_text=_(
            """Add tags. Separate tags by using "Enter" or comma.
        You can add maximum 3 tags, and length of tags should be less than 25
        symbols."""
        ),
    )
    objects = NoteManager()

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

    @property
    def preview_text(self) -> str:
        """Get body preview text for a note."""
        return "".join(
            BeautifulSoup(self.body_html, features="html.parser").findAll(
                text=True
            )
        )

    @property
    def first_image_url(self) -> Optional[str]:
        """Get first image `src` from body text."""
        image = BeautifulSoup(self.body_html, features="html.parser").find(
            name="img"
        )
        if image:
            return image.get("src")

    def generate_md_file(self) -> io.BytesIO:
        output = f"# {self.title}\n\n"
        if self.source and self.source.link:
            output += f"Source: [{self.source.title}]({self.source.link})\n\n"
        elif self.source:
            output += f"Source: __{self.source.title}__\n\n"
        output += self.body_raw
        return io.BytesIO(output.encode())

    def generate_html_file(self) -> io.BytesIO:
        output = "<html><head><meta content='text/html;charset=UTF-8' \
            http-equiv='content-type' /></head><body>"
        output += f"<h1>{self.title}</h1>\n"
        if self.source and self.source.link:
            output += f"<p>Source: <a href='{self.source.link}'>{self.source.title}</a></p>\n"
        elif self.source:
            output += f"<p>Source: {self.source.title}</p>\n"
        output += self.body_html + "</body></html>"
        return io.BytesIO(output.encode())

    def generate_pdf_file(self) -> io.BytesIO:
        html = self.generate_html_file().read().decode(encoding="utf-8")
        options = {"page-size": "Letter", "encoding": "UTF-8"}
        pdf = pdfkit.from_string(html, False, options=options)
        return io.BytesIO(pdf)

    def generate_file(self, filetype: str = "md") -> Optional[io.BytesIO]:
        if filetype == "md":
            return self.generate_md_file()
        elif filetype == "html":
            return self.generate_html_file()
        elif filetype == "pdf":
            return self.generate_pdf_file()
        return None

    def generate_file_to_response(
        self, filetype: str = "md"
    ) -> Optional[dict]:
        filename = self.slug[:20] + "." + filetype
        file = self.generate_file(filetype=filetype)
        if not file:
            return None
        content_type = {
            "md": "text/markdown; charset=UTF-8",
            "html": "text/html; charset=utf-8",
            "pdf": "application/pdf",
        }[filetype]
        return {
            "file": file,
            "filename": filename,
            "content_type": content_type,
        }

    def get_fork(self):
        return Note(
            title=self.title,
            source=self.source,
            body_raw=self.body_raw,
            body_html=self.body_html,
            summary=self.summary,
            tags=self.tags,
            fork=self,
        )

    def get_similar_by_tags(self) -> QuerySet:
        """Get notes with similar tag.

        Returns QuerySet of notes with similar tags for a note ordered by
        number of common tags and creation datetime.
        """
        note_tags_ids = self.tags.values_list("id", flat=True)
        similar_notes = (
            Note.objects.public()
            .filter(tags__in=note_tags_ids)
            .exclude(id=self.id)
        )
        similar_notes = similar_notes.annotate(
            same_tags=Count("tags")
        ).order_by("-same_tags", "-datetime_created")
        return similar_notes

    @property
    def this_year(self) -> bool:
        return date.today().year == self.modified.year

    @property
    def is_modified(self) -> bool:
        return self.created.date() != self.modified.date()

    @property
    def min_read(self) -> int:
        """Return how many minutes required to read the note.

        Average ru word length = 7,2
        Average en word length = 5,2
        Average wpm reading speed = 150
        """
        return int((len(self.body_raw) + 1) / ((7.2 + 5.2) / 2) // 150)
