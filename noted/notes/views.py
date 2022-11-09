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
    notes_search: search notes instances by a GET request query.
    note_like: like/unlike a note.
    handler404: handels error 404 code.

"""

from taggit.models import Tag

from django.views import View
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import (SearchVector, SearchQuery,
    SearchRank, TrigramSimilarity, SearchHeadline)
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
    FormView)                       
from django.views.generic.edit import DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.urls import reverse, reverse_lazy

from notes.forms import NoteForm, CommentForm, SearchForm, comment_form_factory
from notes.models import Note
from user.models import User


class NoteList(ListView):
    """Display a list of :model:`notes.Note`.

    Uses as a superclass for other specific notes listings.

    Notes order options (provides through a GET param `order`):
        `datetime_created`: from oldest to newest by publish date.
        `-datetime_created`: from newest to oldest by publish date.
        `comments`: from the most commented to the least commented notes. 
        `users_like`: from the most number of likes to the least.

    **Context**
        notes: a queryset of :model:`notes.Note` instances.
        paginator: a paginator for notes list.
        page_obj: a pagination navigator.
        order_label: a human readable label of a notes order option.

    """
    ORDER_LABELS = {
        'datetime_created': 'Oldest',
        '-datetime_created': 'Latest',
        'comments': 'Most Commented',
        'users_like': 'Most Liked',
    }
    model = Note
    context_object_name = 'notes'
    paginate_by = 18

    def get_ordering(self):
        return self.request.GET.get('order', default='-datetime_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_ordering()
        context['order_label'] = self.ORDER_LABELS.get(order, '')
        return context

    def get_ordered_queryset(self, queryset):
        """Order a queryset by GET param `order`"""
        if not queryset:
            queryset = super().get_queryset()
        order = self.get_ordering()
        if order == 'comments':
            queryset = queryset.annotate(
                count=Count('comments')
            ).order_by('-count')
        else:
            queryset = queryset.order_by(order)
        return queryset


class PublicNoteList(NoteList):
    """Display a list of :model:`notes.Note` available for every one.

    It displays the home page of the website. A list consists of all notes
    except private notes.

    **Context**
        notes: a queryset of :model:`notes.Note` instances.
        paginator: a paginator for notes list.
        page_obj: a pagination navigator.
        order_label: a human readable label of a notes order option.
        most_liked: 5 most liked notes.
        most_commented: 5 most commented notes.

    **Template**
        :template:`frontend/templates/notes/public_list.html`

    """
    template_name = 'notes/public_list.html'

    def get_queryset(self):
        queryset = Note.objects.public()
        return super().get_ordered_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['most_liked'] = Note.objects.most_liked()[:5]
        context['most_commented'] = Note.objects.most_commented()[:5]
        return context


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
        queryset = Note.objects.personal(self.request.user)
        return super().get_ordered_queryset(queryset)


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
        queryset = Note.objects.public().filter(tags=tag)
        return super().get_ordered_queryset(queryset)

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
        queryset = Note.objects.personal(user)
        queryset = queryset.filter(private=False, anonymous=False)
        return super().get_ordered_queryset(queryset)


class NoteDetailView(DetailView, MultipleObjectMixin):
    """Display details of a :model:`notes.Note` instance.

    **Context**
        note: a :model:`notes.Note` instance.
        paginator: a paginator for comments list.
        page_obj: a pagination navigator.
        comment_form: a form for creating a comment.
        notes: notes with common tags to a current note.

    **Template**
        :template:`frontend/templates/notes/note.html`

    """
    model = Note
    context_object_name = 'note'
    template_name = 'notes/note.html'
    paginate_by = 7

    def get_context_data(self, **kwargs):
        note = self.get_object()
        # Get root comments and add to the context
        root_comments = note.comments.filter(parent=None)
        context = super(
            NoteDetailView, self
        ).get_context_data(object_list=root_comments, **kwargs)
        # Create a comment form for current comments and add to the context
        context['comment_form'] = comment_form_factory(root_comments)
        # Сontext name `notes` is vulnerable
        context['notes'] = note.get_similar_by_tags()[:4]
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

    def post(self, request, *args, **kwargs):
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

    It uses two different class based views with the same URL. We have
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


def notes_search(request):
    """Search :model:`notes.Note` instances by a GET request query.
        
    **Context**
        form: a form for a search query.
        query: a search query.
        notes: a search result.

    **Template**
        :template:`frontend/templates/notes/search.html`
        
    """
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + \
                            SearchVector('summary', weight='A') + \
                            SearchVector('body_raw', weight='B')
            search_query = SearchQuery(query)
            headline = SearchHeadline('title', search_query,
                                      start_sel=u'<mark>', stop_sel=u'</mark>')
            results = Note.objects.public().annotate(
                    rank=SearchRank(search_vector, search_query),
                    similarity=TrigramSimilarity('title', query),
                    headline=headline
                ).filter(
                    Q(rank__gte=0.2) | Q(similarity__gt=0.1)
            ).order_by('-rank')
    return render(request, 'notes/search.html',
                  {'form': form,  'query': query, 'notes': results})


@login_required(login_url=reverse_lazy('account_login'))
@require_POST
def note_like(request):
    """Like/unlike a note via a ajax request."""
    note_id = request.POST.get('id')
    action = request.POST.get('action')
    if note_id and action:
        try:
            note = Note.objects.get(id=note_id)
            if action == 'like':
                note.users_like.add(request.user)
            else:
                note.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})


def handler404(request, *args, **kwargs):
    return render(request, '404.html', {}, status=404)
