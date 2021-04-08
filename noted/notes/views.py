from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.decorators.http import require_GET
from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from taggit.models import Tag

from notes.forms import NoteForm
from notes.models import Note


class NoteList(ListView):
    ORDER_LABELS = {
        'date': 'Oldest',
        '-date': 'Latest',
    }
    model = Note
    context_object_name = 'notes'
    paginate_by = 18
    template_name = 'notes/list.html'

    def get_ordering(self):
        order = self.request.GET.get('order', '-date')
        if order.replace('-', '', 1) == 'date':
            return order
        return '-date'

    def get_context_data(self, *args, **kwargs):
        order = self.get_ordering()
        context = super().get_context_data(**kwargs)
        context['order_label'] = self.ORDER_LABELS.get(order, '')
        return context


class PersonalNoteList(NoteList):
    template_name = 'notes/personal_list.html'

    def get_queryset(self):
        queryset = Note.get_personal_notes(self.request.user)
        order = self.get_ordering()
        return queryset.order_by(order)


class TaggedNoteListView(NoteList):
    template_name = 'notes/tagged_list.html'

    def get_queryset(self):
        if 'tag_slug' in self.kwargs:
            slug = self.kwargs['tag_slug']
            tag = get_object_or_404(Tag, slug=slug)
            setattr(self, 'tag', tag)
        else:
            raise Http404('The tag slug wasn\'t found.')
        queryset = Note.objects.filter(tags=tag)
        order = self.get_ordering()
        return queryset.order_by(order)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class NoteDetailView(DetailView):
    model = Note
    context_object_name = 'note'
    template_name = 'notes/note.html'


@method_decorator(login_required, name='dispatch')
class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/update.html'


@method_decorator(login_required, name='dispatch')
class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('home')
