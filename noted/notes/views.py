from django.views import View
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, FormView
)                       
from django.views.generic.edit import DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy

from taggit.models import Tag

from notes.forms import NoteForm, CommentForm
from notes.models import Note, Comment
from user.models import User


class NoteList(ListView):
    ORDER_LABELS = {
        'date': 'Oldest',
        '-date': 'Latest',
        'comments': 'Most Commented'
    }
    model = Note
    context_object_name = 'notes'
    paginate_by = 18

    def get_ordering(self):
        return self.request.GET.get('order', default='-date')

    def get_context_data(self, *args, **kwargs):
        order = self.get_ordering()
        context = super().get_context_data(**kwargs)
        context['order_label'] = self.ORDER_LABELS.get(order, '')
        return context


class PublicNoteList(NoteList):
    template_name = 'notes/public_list.html'

    def get_queryset(self):
        queryset = Note.objects.filter(private=False)
        if self.request.user.is_authenticated:
            user = self.request.user
            personal_queryset = Note.objects.get_personal_notes(user)
            queryset = queryset | personal_queryset
        
        order = self.get_ordering()
        if order == 'comments':
            queryset = queryset.annotate(
                count=Count('comments')
            ).order_by('-count')
        else:
            queryset = queryset.order_by(order)
        
        return queryset


@method_decorator(login_required, name='dispatch')
class PersonalNoteList(NoteList):
    template_name = 'notes/personal_list.html'

    def get_queryset(self):
        queryset = Note.objects.get_personal_notes(self.request.user)
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
        queryset = Note.objects.filter(tags=tag, private=False)
        order = self.get_ordering()
        return queryset.order_by(order)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class UserNoteListView(NoteList):
    template_name = 'notes/by_user_list.html'

    def get_queryset(self):
        if 'username' in self.kwargs:
            username = self.kwargs['username']
            user = get_object_or_404(User, username=username)
        else:
            raise Http404(
                'The user with name "{}" wasn\'t found.'.format(username)
            )
        queryset = Note.objects.get_personal_notes(user)
        queryset = queryset.filter(private=False).filter(anonymous=False)
        order = self.get_ordering()
        return queryset.order_by(order)


class NoteDetailView(DetailView, MultipleObjectMixin):
    model = Note
    context_object_name = 'note'
    template_name = 'notes/note.html'
    paginate_by = 7

    def get_context_data(self, *args, **kwargs):
        object_list = Comment.objects.filter(
            note=self.get_object(), parent=None
        )
        context = super(NoteDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['comment_form'] = CommentForm()
        return context


class CommentFormView(SingleObjectMixin, FormView):
    template_name = 'notes/note.html'
    form_class = CommentForm
    model = Note

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            author = get_object_or_404(User, id=request.user.id)
            form.instance.author = author
            form.instance.note = self.object
            form.instance.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return "%s?page=%s" % (
            reverse('note', kwargs={'slug': self.object.slug}),
            self.request.GET.get('page', default='1')
        )


class NoteView(View):

    def get(self, request, *args, **kwargs):
        view = NoteDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentFormView.as_view()
        return view(request, *args, **kwargs)


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
