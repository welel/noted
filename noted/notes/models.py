from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Note(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    source = models.URLField(blank=True, default='')
    body = models.TextField(max_length=20000, blank=True, default='')

    def __str__(self):
        return self.title
