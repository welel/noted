from django.views.generic import ListView, DetailView

from notes.models import Note


class NoteList(ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'notes/home.html'


class NoteDetailView(DetailView):
    model = Note
    context_object_name = 'note'
    template_name = 'notes/note.html'
