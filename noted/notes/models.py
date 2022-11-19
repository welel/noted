"""Models of the the `notes` app.

**Models**
    Note (Model): a Markdown text with a list of attributes.
    Comment (MPTTModel): a comment for a note.

"""
import uuid

from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey

from django.core.exceptions import FieldError
from django.db import models
from django.db.models import QuerySet, Count
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from markdown.fields import MarkdownField, RenderedMarkdownField
from tags.models import UnicodeTaggedItem
from user.models import User


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
        return self.filter(private=False)

    def most_liked(self, all: bool=True, public: bool=False) -> QuerySet:
        """Query notes sorted by number of likes from the most to least.
        
        Params:
            all: if false includes only notes that have at least one like.
            public: if true excludes private notes. 
        """
        queryset = self.annotate(count=Count('users_like')).order_by('-count')
        if public:
            queryset = queryset.filter(private=False)
        if not all:
            return queryset.filter(count__gt=0)
        return queryset

    def most_commented(self, all : bool=True, public: bool=False) -> QuerySet:
        """Query notes sorted by number of comments from the most to least.
        
        Params:
            all: if false includes only notes that have at least one comment.
            public: if true exclude private notes. 
        """
        queryset = self.annotate(count=Count('comments')).order_by('-count')
        if public:
            queryset = queryset.filter(private=False)
        if not all:
            return queryset.filter(count__gt=0)
        return queryset

    def datetime_created(self):
        return self.order_by('datetime_created')

    def datetime_created_dec(self):
        return self.order_by('-datetime_created')


class Note(models.Model):
    """Markdown text with a list of attributes.
    
    **Fields**
        title: a title of a note.
        slug: a slug of a note for URL.
        author: a user foreign key, author of a note.
        source: a link to a source of a note.
        body_raw: a raw Markdown text from a form.
        body_html: HTML representation of `body_raw`, it is generated
                   based on `body_raw` via GitHub API.
        summary: a short summary on a text of a note.
        private: a boolean flag makes a notes private (hides from other users). 
        anonymous: a boolean flag hides an author of a note.
        allow_comments: a boolean flag allows to users leave comments
                        to a note.
        datetime_created: publish datetime of a note.
        datetime_modified: update datetime of a note.
        tags: tags of a note (max tags - 5, max length - 24 symbols).
        users_like: a m2m field for note likes.
        favourites: a m2m field for bookmarks for user.
    
    """

    title = models.CharField(max_length=100, null=False, blank=False,
        db_index=True)
    slug = models.SlugField(max_length=255, editable=False, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, editable=False
    )
    source = models.URLField(
        blank=True, default='',
        help_text=_('Place a link to the source to which you are taking notes.')
    )
    body_raw = MarkdownField(rendered_field='body_html')
    body_html = RenderedMarkdownField(max_length=40000, default='', blank=True)
    summary = models.CharField(
        max_length=100, default='', blank=True,
        help_text=_('Write summary on the note in 100 symbols.')
    )
    private = models.BooleanField(
        default=False, help_text=_('Only you can see the note.')
    )
    anonymous = models.BooleanField(
        default=False, help_text=_('Others won\'t see that the note is yours.')
    )
    allow_comments = models.BooleanField(
        default=True, help_text=_('Allow users to leave comments.')
    )
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager(
        through=UnicodeTaggedItem, blank=True, related_name='notes',
        help_text=_('''Add tags. Separate tags by using "Enter" or comma.
        You can add maximum 5 tags, and length of tags should be less than 25
        symbols.''')
    )
    users_like = models.ManyToManyField(User, related_name='notes_liked',
                                        blank=True)
    favourites = models.ManyToManyField(User, related_name='favourites',
        default=None, blank=True)
    objects = NoteManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self._generate_unique_slug()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('note', args=[self.slug, ])

    def _generate_unique_slug(self) -> str:
        """Generate unique slug for ``Note`` instance and return it.

        The method slugifys `title` and adds random symbols
        at the end if `slug` isn't unique.

        """
        if not self.title:
            raise FieldError(
                'Cannot generate `slug`, because `title` is empty.'
            )
        slug = slugify(self.title, allow_unicode=True)[:247]
        try:
            note = Note.objects.get(slug=slug)
        except Note.DoesNotExist:
            return slug
        if note.id == self.id:
            return note.slug
        else:
            slug += str(uuid.uuid1())[:8]
            return slug[:255]

    def get_similar_by_tags(self) -> QuerySet:
        """Get notes with similar tag.
        
        Returns QuerySet of notes with similar tags for a note ordered by
        number of common tags and creation datetime. 
        """
        note_tags_ids = self.tags.values_list('id', flat=True)
        similar_notes = Note.objects.public().filter(
            tags__in=note_tags_ids).exclude(id=self.id)
        similar_notes = similar_notes.annotate(
            same_tags=Count('tags')).order_by('-same_tags',
                                              '-datetime_created')
        return similar_notes


class Comment(MPTTModel):
    """Comment of ``Note`` instance.

    TODO: add ability to delete. 

    Comments have a tree system with 2 levels: root and child. A comment
    is root if it was written directly to a note. And a comment is a child,
    if it replies to another comment. If a comment reply on a root comment,
    first one becomes a child of second one. If a comment replies to a child
    comment, first one becomes a child of parent of second one. Therefore
    there are only 2 levels.
    
    **Fields**
        note: a foreign key to a commented note.
        parent: tree foreign key to a parent comment.
        author: a user foreign key, author of a comment.
        content: a text of a comment.
        date: a publish datetime.
    
    """

    note = models.ForeignKey(Note, on_delete=models.CASCADE,
                             related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children',
                            db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    content = models.TextField(max_length=2000)
    date = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['date']

    def __str__(self):
        return f'Comment by {self.author}'
