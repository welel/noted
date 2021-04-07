from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from notes.models import Note


class NoteList(ListView):
    model = Note
    context_object_name = 'notes'
    paginate_by = 18
    template_name = 'notes/home.html'

    def get_ordering(self):
        order = self.request.GET.get('order', '-data')
        if order.replace('-', '', 1) in ['id', 'data']:
            return order
        return '-data'


class PersonalNoteList(NoteList):
    template_name = 'notes/personal_notes.html'

    def get_queryset(self):
        queryset = Note.get_personal_notes(self.request.user)
        order = self.get_ordering()
        return queryset.order_by(order)


class NoteDetailView(DetailView):
    model = Note
    context_object_name = 'note'
    template_name = 'notes/note.html'


@method_decorator(login_required, name='dispatch')
class NoteCreateView(CreateView):
    model = Note
    fields = ['title', 'source', 'private', 'anonymous', 'body_raw']
    template_name = 'notes/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class NoteUpdateView(UpdateView):
    model = Note
    fields = ['title', 'source', 'private', 'anonymous', 'body_raw']
    template_name = 'notes/update.html'


@method_decorator(login_required, name='dispatch')
class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('home')
