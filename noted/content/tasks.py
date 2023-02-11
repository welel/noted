import time
from typing import Type
import uuid

from celery import shared_task

from django.core.cache import cache
from django.http import HttpResponse

from .models import Note


@shared_task
def generate_file_response_task(note_pk: int, filetype: str):
    note = Note.objects.get(pk=note_pk)
    return note.generate_file(filetype=filetype)
