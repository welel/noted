u""""Views for the `notes` app.

**Views**
    NoteList: a superclass for note listing.
        ├── PublicNoteList: displays a list of public notes.
        ├── PersonalNoteList: displays a list of a logged-in user notes.
        ├── TaggedNoteListView: displays a list of notes with a common tag.
        └── UserNoteListView: displays a list of selected user notes.
    NoteView: a selector of a view between 2 views below.
        ├── NoteDetailView: displays note details.
        └── CommentFormView: handles a comment form on a note details page.
    NoteCreateView: handles creating of a note.
    NoteUpdateView: handles editing of a note.
    NoteDeleteView: handles deletion of a note.

"""

from taggit.models import Tag

from django.views import View
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
    FormView)                       
from django.views.generic.edit import DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy

from notes.forms import NoteForm, CommentForm, comment_form_factory
from notes.models import Note
from user.models import User


class NoteList(ListView):
    """Display a list of :model:`notes.Note`.

    Uses as a superclass for other specific notes listings.

    Notes order options (provides through a GET param `order`):
        `date`: from oldest to newest by publish/update date.
        `-date`: from newest to oldest by publish/update date.
        `comments`: from the most commented to the least commented notes. 

    **Context**
        notes: a queryset of :model:`notes.Note` instances.
        paginator: a paginator for notes list.
        page_obj: a pagination navigator.
        order_label: a human readable label of a notes order option.

    """
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_ordering()
        context['order_label'] = self.ORDER_LABELS.get(order, '')
        return context


class PublicNoteList(NoteList):
    """Display a list of :model:`notes.Note` available for every one.

    It displays the home page of the website. A list consists of all notes
    except private notes.

    TODO: Now handles ordering (put ordering in the supercalss).

    **Context**
        notes: a queryset of :model:`notes.Note` instances.
        paginator: a paginator for notes list.
        page_obj: a pagination navigator.
        order_label: a human readable label of a notes order option.

    **Template**
        :template:`frontend/templates/notes/public_list.html`

    """
    template_name = 'notes/public_list.html'

    def get_queryset(self):
        queryset = Note.objects.filter(private=False)
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
    """Display a list of :model:`notes.Note` of a logged-in user.

    **Context**
        notes: a queryset of :model:`notes.Note` instances.
        paginator: a paginator for notes list.
        page_obj: a pagination navigator.
        order_label: a human readable label of a notes order option.

    **Template**
        :template:`frontend/templates/notes/personal_list.html`

    """
    template_name = 'notes/personal_list.html'

    def get_queryset(self):
        queryset = Note.objects.get_personal_notes(self.request.user)
        order = self.get_ordering()
        return queryset.order_by(order)


class TaggedNoteListView(NoteList):
    """Display a list of :model:`notes.Note` with a selected common tag.

    **Context**
        notes: a queryset of :model:`notes.Note` instances.
        paginator: a paginator for notes list.
        page_obj: a pagination navigator.
        order_label: a human readable label of a notes order option.
        tag: a selected tag instance :model:`taggit.Tag`.

    **Template**
        :template:`frontend/templates/notes/tagged_list.html`

    """
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class UserNoteListView(NoteList):
    """Display a list of public :model:`notes.Note` of a selected user.

    **Context**
        notes: a queryset of :model:`notes.Note` instances.
        paginator: a paginator for notes list.
        page_obj: a pagination navigator.
        order_label: a human readable label of a notes order option.

    **Template**
        :template:`frontend/templates/notes/by_user_list.html`

    """
    template_name = 'notes/by_user_list.html'

    def get_queryset(self):
        if 'username' in self.kwargs:
            username = self.kwargs['username']
            user = get_object_or_404(User, username=username)
        else:
            raise Http404(
                f'The user with name "{username}" wasn\'t found.'
            )
        queryset = Note.objects.get_personal_notes(user)
        queryset = queryset.filter(private=False, anonymous=False)
        order = self.get_ordering()
        return queryset.order_by(order)


class NoteDetailView(DetailView, MultipleObjectMixin):
    """Display details of a :model:`notes.Note` instance.

    **Context**
        note: a :model:`notes.Note` instance.
        paginator: a paginator for comments list.
        page_obj: a pagination navigator.
        comment_form: a form for creating a comment.

    **Template**
        :template:`frontend/templates/notes/note.html`

    """
    model = Note
    context_object_name = 'note'
    template_name = 'notes/note.html'
    paginate_by = 7

    def get_context_data(self, **kwargs):
        note = self.get_object()
        object_list = note.comments.filter(parent=None)
        context = super(
            NoteDetailView, self
        ).get_context_data(object_list=object_list, **kwargs)
        context['comment_form'] = comment_form_factory(object_list)
        return context


@method_decorator(login_required, name='dispatch')
class CommentFormView(SingleObjectMixin, FormView):
    """Handle POST request to ``CommentForm``, creates a comment.
    
    TODO: save text of a comment if redirected after loggining.
        
    **Template**
        :template:`frontend/templates/notes/note.html`

    """
    template_name = 'notes/note.html'
    form_class = CommentForm
    model = Note

    def post(self, request):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            author = get_object_or_404(User, id=request.user.id)
            form.instance.author = author
            form.instance.note = self.object
            form.instance.save()
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return "{url}?page={page_num}".format(
            url=reverse('note', kwargs={'slug': self.object.slug}),
            page_num=self.request.GET.get('page', default='1')
        )


class NoteView(View):
    """Chose a view based on a request method (GET/POST).

    It uses two different class based views from the same URL. We have
    a division here: GET requests should get the ``NoteDetailView`` (with
    a form added to the context data), and POST requests should get
    the ``CommentFormView``.

    """

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
