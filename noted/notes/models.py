import uuid

from django.core.exceptions import FieldError
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


User = get_user_model()


class Note(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(max_length=254, editable=False, unique=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    source = models.URLField(blank=True, default='')
    body = models.TextField(max_length=20000, blank=True, default='')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        return super().save(*args, **kwargs)

    def _generate_unique_slug(self) -> str:
        if not self.title:
            raise FieldError(
                'Cannot generate `slug`, because `title` is empty.'
            )
        slug = slugify(self.title, allow_unicode=True)
        if Note.objects.filter(slug=slug).exists():
            slug += str(uuid.uuid1())[:8]
        return slug
