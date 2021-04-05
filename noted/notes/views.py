from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from notes.models import Note


class NoteList(ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'notes/home.html'


class NoteDetailView(DetailView):
    model = Note
    context_object_name = 'note'
    template_name = 'notes/note.html'


@method_decorator(login_required, name='dispatch')
class NoteCreateView(CreateView):
    model = Note
    fields = ['title', 'source', 'body_raw']
    template_name = 'notes/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class NoteUpdateView(UpdateView):
    model = Note
    fields = ['title', 'source', 'body_raw']
    template_name = 'notes/update.html'


@method_decorator(login_required, name='dispatch')
class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('home')
