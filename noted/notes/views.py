from django.views.generic import ListView

from notes.models import Note


class NoteList(ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'notes/home.html'
