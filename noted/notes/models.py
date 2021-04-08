import requests
import uuid

from django.core.exceptions import FieldError
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

from simplemde.fields import SimpleMDEField


User = get_user_model()


class NoteManager(models.Manager):

    def new_order(self):
        return self.earliest('date')

    def old_order(self):
        return self.latest('date')


class Note(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(max_length=254, editable=False, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, editable=False
    )
    source = models.URLField(
        blank=True, default='',
        help_text='Place a link to the source to which you are taking notes.'
    )
    body_raw = SimpleMDEField()
    body_html = models.TextField(max_length=40000, default='', blank=True)
    private = models.BooleanField(
        default=False, help_text='Only you can see the note.'
    )
    anonymous = models.BooleanField(
        default=False, help_text='Others won\'t see that the note is yours.'
    )
    date = models.DateTimeField(auto_now=True)
    objects = NoteManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self._generate_unique_slug()[:254]
        self.body_html = self._get_body_html()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('note', args=[self.slug, ])

    @classmethod
    def get_personal_notes(cls, user):
        return cls.objects.filter(author=user)

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
        return slug

    def _get_body_html(self) -> str:
        """Makes POST request to GitHub API for html code.

        API docs: https://docs.github.com/en/rest/reference/markdown
        Sends `body_raw` in body of POST request to GitHub API.
        Gets html code of markdown text (from `body_raw`) and
        returns it.

        """
        url = 'https://api.github.com/markdown/raw'
        headers = {'Content-Type': 'text/plain'}
        data = self.body_raw.encode('utf-8', 'ignore')
        if isinstance(data, bytes):
            try:
                response = requests.post(url, data=data, headers=headers)
            except requests.exceptions.ConnectionError:
                return self.body_raw
            if response.status_code == 200:
                return response.text
        return self.body_raw
