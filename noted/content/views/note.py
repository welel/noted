"""Views for :model:`Note`.


**Views**
    NoteList: a superclass for note listing.
        ├── WelcomeNoteList: welcome page for unlogged users (with note list).
        ├── PublicNoteList: displays a list of public notes.
        ├── ProfileNoteList: displays a list of public of a selected user.
        └── PersonalNoteList: display a list of all user's notes.
    NoteView: a selector of a view between 2 views below (in future).
        1. NoteDetailView: displays note details.
        2. [Comments in future]
    NoteCreateView: handles creating of a note.
    NoteForkView: handles creating of a fork note.
    NoteUpdateView: handles editing of a note.
    NoteDeleteView: handles deletion of a note.
    pin_note: pin/unpin a note.
    like_note: like/unlike a note.
    bookmark_note: add/delete a note to/from user's bookmarks.
    download_note: download a note as a file.

"""
import logging
from wsgiref.util import FileWrapper

from taggit.models import Tag

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import F, QuerySet
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView

from actions import base as act
from actions.models import Action
from common import logging as log
from common.cache import cache_queryset
from common.decorators import ajax_required
from content.forms import NoteForm
from content.models import Note, Source
from tags.models import get_top_tags
from users.models import Following, User


logger = logging.getLogger(__name__)


class NoteList(ListView):
    """Base display list of :model:`Note`.

    Uses as a superclass for other specific notes listings.

    Notes order options (provides through a GET param `order`):
        `-datetime_created`: From newest to oldest by publish date.
        `views`: From the most viewed to the least.
        `likes`: From the most liked to the least.

    **Context**
        notes: A queryset of :model:`notes.Note` instances.
        paginator: A paginator for notes list.
        page_obj: A pagination navigator.

    """

    SORTING_FUNCS_MAPPING = {
        "-datetime_created": Note.objects.by_created,
        "views": Note.objects.popular,
        "likes": Note.objects.most_liked,
    }

    model = Note
    context_object_name = "notes"
    paginate_by = 100

    def get_ordering(self) -> str:
        """Gets a `order` option from GET params and returns it."""
        return self.request.GET.get("order", default="-datetime_created")

    def get_ordered_queryset(self) -> QuerySet:
        """Orders a queryset by a order option."""
        return self.SORTING_FUNCS_MAPPING[self.get_ordering()]()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context[
                "user_bookmarks"
            ] = self.request.user.bookmarked_notes.all()
        return context


@method_decorator(cache_page(60 * 60), name="dispatch")
class WelcomeNoteList(NoteList):
    """Welcome page for unlogged users.

    **Context**
        source_types: All source types of `Source`.
        trends: Top 6 popular notes (by views).
        tags: Top 7 tags (by number of notes).

    **Template**
        :template:`frontend/templates/welcome.html`

    """

    template_name = "welcome.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("content:home")
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_ordered_queryset().filter(draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["source_types"] = dict(Source.TYPES)
        trends = cache_queryset(259200)(Note.objects.popular)()[:6]
        for i, trend in enumerate(trends):
            context[f"trend_{i+1}"] = trend
        context["tags"] = cache_queryset(259200)(get_top_tags)(12)
        return context


class PublicNoteList(LoginRequiredMixin, NoteList):
    """Display a list of :model:`Note` available for every one.

    It displays the home page of the website. A list consists of all notes
    except drafts.

    **Context**
        source_types: All source types.
        sidenotes: A recommended note list.
        tags: Top 7 tags (by number of notes).
        tags_notes: A note list with tags to which the user is subscribed.
        following_notes: A note list of users to which the user is subscribed.

    **Template**
        :template:`frontend/templates/index.html`

    """

    template_name = "index.html"
    login_url = "content:welcome"
    redirect_field_name = "content:home"

    def get_queryset(self):
        return super().get_ordered_queryset().filter(draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["source_types"] = dict(Source.TYPES)
        context["sidenotes"] = cache_queryset(259200)(Note.objects.popular)()[
            :5
        ]
        context["tags"] = cache_queryset(259200)(get_top_tags)(7)
        if self.request.user.is_authenticated:
            context["following_notes"] = Note.objects.optimize().filter(
                author__in=Following.objects.get_following(self.request.user),
                draft=False,
                anonymous=False,
            )
            context["tags_notes"] = Note.objects.tags_in(
                self.request.user.profile.tags.names()
            )
        return context


class ProfileNoteList(NoteList):
    """Display a list of public :model:`Note` of a selected user.

    It displays the profile page of the specifiec user (only public notes).

    **Context**
        user: The selected user.
        pins: User's pins (note list).
        sidenotes: A recommended note list.
        followers: User's followers.
        total_user_likes:Total like number of all user's notes.

    **Template**
        :template:`frontend/templates/content/note_list_profile.html`

    """

    template_name = "content/note_list_profile.html"

    def get(self, request, slug, *args, **kwargs):
        if request.user.is_authenticated and request.user.slug == slug:
            return redirect("content:personal_notes", *args, **kwargs)
        return super().get(request, slug, *args, **kwargs)

    def get_queryset(self):
        username = User.unslugify(self.kwargs.get("slug"))
        user = get_object_or_404(User, username=username)
        return (
            super()
            .get_ordered_queryset()
            .filter(author=user, draft=False, anonymous=False)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = User.unslugify(self.kwargs.get("slug"))
        user = get_object_or_404(User, username=username)
        context["user"] = user
        context["pins"] = self.get_queryset().filter(pin=True)
        context["sidenotes"] = cache_queryset(259200)(Note.objects.popular)()[
            :5
        ]
        context["followers"] = [
            contact.follower
            for contact in Following.objects.filter(followed=user)
        ]
        context["total_user_likes"] = sum(
            [note.likes.all().count() for note in self.get_queryset()]
        )
        return context


class PersonalNotesView(LoginRequiredMixin, NoteList):
    """Display a list of all user's notes.

    **Context**
        user: The selected user.
        pins: User's pins (note list).
        drafts: User's drafts (note list).
        bookmarks: Users's bookmarks (note list).
        sidenotes: A recommended note list.

    **Template**
        :template:`frontend/templates/content/note_list_personal.html`

    """

    template_name = "content/note_list_personal.html"

    def get_queryset(self):
        return super().get_ordered_queryset().filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context.update(
            {
                "user": self.request.user,
                "notes": qs.filter(draft=False),
                "pins": qs.filter(pin=True),
                "drafts": qs.filter(draft=True),
                "bookmarks": self.request.user.bookmarked_notes.all(),
                "sidenotes": cache_queryset(259200)(Note.objects.popular)()[
                    :5
                ],
            }
        )
        return context


class NoteDraftMixin:
    """Manages saving of a note based on pressed button (publish or draft).

    The form has 2 butons - publish, draft. If the draft button was pressed
    the `draft` note field sets as True, else as False.
    """

    def form_valid(self, form):
        form.instance.draft = self.draft
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.draft = "savedraft" in request.POST
        return super().post(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class NoteCreateView(NoteDraftMixin, CreateView):
    """Handels the note create form."""

    model = Note
    form_class = NoteForm
    template_name = "content/note_create.html"

    def add_initial_source(self, slug: str, initial: dict) -> dict:
        """Prepopulates the form with `Source` data."""
        try:
            source = Source.objects.get(slug=slug)
        except Source.DoesNotExist:
            return initial
        initial.update(
            {
                "source": source.title,
                "source_type": source.type,
                "source_link": source.link,
                "source_description": source.description,
            }
        )
        return initial

    def add_initial_tag(self, slug: str, initial: dict) -> dict:
        """Prepopulates the form with a tag."""
        try:
            tag = Tag.objects.get(slug=slug)
        except Tag.DoesNotExist:
            return initial
        initial["tags"] = tag.name
        return initial

    def get_initial(self):
        initial = super().get_initial()
        source_slug = self.request.GET.get("source")
        tag_slug = self.request.GET.get("tag")
        if source_slug:
            initial = self.add_initial_source(source_slug, initial)
        if tag_slug:
            initial = self.add_initial_tag(tag_slug, initial)
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class NoteForkView(NoteCreateView):
    """Handles the create note form (for forked note)."""

    def get_initial(self):
        initial = super().get_initial()
        try:
            note = Note.objects.get(slug=self.kwargs.get("slug"))
        except Source.DoesNotExist:
            return initial
        self.object = note.get_fork()
        if note.source:
            initial = super().add_initial_source(note.source.slug, initial)
        if note.tags:
            initial["tags"] = note.tags.all()
        return initial


@method_decorator(login_required, name="dispatch")
class NoteUpdateView(NoteDraftMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "content/note_create.html"


@method_decorator(login_required, name="dispatch")
class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy("content:home")


class NoteDetailsView(DetailView):
    """Display details of a :model:`Note` instance.

    **Context**
        sidenotes: A recommended note list.

    **Template**
        :template:`frontend/templates/content/note_display.html`

    """

    model = Note
    template_name = "content/note_display.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidenotes"] = cache_queryset(259200)(Note.objects.popular)()[
            :5
        ]
        return context

    def get_object(self):
        note = super().get_object()
        if note and self.request.user != note.author:
            Note.objects.filter(pk=note.pk).update(views=F("views") + 1)
        return note


class NoteView(View):
    """Choose a view based on a request method (GET/POST).

    For future: it will choose between GET - the details view and
    POST - the comment form handler.
    """

    def get(self, request, *args, **kwargs):
        view = NoteDetailsView.as_view()
        return view(request, *args, **kwargs)


@require_GET
@login_required(login_url=reverse_lazy("account_login"))
@ajax_required()
def pin_note(request, slug):
    """Sets `pin` note field via an ajax request."""
    note = get_object_or_404(Note, slug=slug)
    if note.author != request.user:
        return HttpResponseBadRequest()
    note.pin = not note.pin
    note.save()
    return JsonResponse({"pin": note.pin})


@require_GET
@login_required(login_url=reverse_lazy("account_login"))
@ajax_required()
def like_note(request, slug):
    """Adds/removes a like to/from a note."""
    note = get_object_or_404(Note, slug=slug)
    if request.user in note.likes.all():
        note.likes.remove(request.user)
        return JsonResponse({"liked": False})
    else:
        note.likes.add(request.user)
        Action.objects.create_action(request.user, act.LIKE, note, notify=True)
        return JsonResponse({"liked": True})


@require_GET
@login_required(login_url=reverse_lazy("account_login"))
@ajax_required()
def bookmark_note(request, slug):
    """Adds/removes a note to/from user's bookmarks."""
    note = get_object_or_404(Note, slug=slug)
    # cache.delete_pattern("*PublicNoteList*")
    if request.user in note.bookmarks.all():
        note.bookmarks.remove(request.user)
        return JsonResponse({"bookmarked": False})
    else:
        note.bookmarks.add(request.user)
        Action.objects.create_action(request.user, act.BOOKMARK, note)
        return JsonResponse({"bookmarked": True})


@require_GET
@login_required(login_url=reverse_lazy("account_login"))
def download_note(request, filetype: str, slug: str):
    """Download a note as a file.

    Attrs:
        filetype: an extension of a required file (md, html, pdf).
        slug: a slug of a note.
    """
    note = get_object_or_404(Note, slug=slug)
    file = note.generate_file_to_response(filetype=filetype)
    if not file or (note.draft and request.user != note.author):
        logger.error(
            log.VIEW_LOG_TEMPLATE.format(
                view=download_note.__name__,
                user=request.user,
                method=request.method,
                path=request.path,
            )
            + "Can't generate a file."
        )
        return HttpResponseBadRequest()
    response = HttpResponse(
        FileWrapper(file["file"]), content_type=file["content_type"]
    )
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{file["filename"]}"'.encode(encoding="utf-8")
    Action.objects.create_action(request.user, act.DOWNLOAD, note)
    return response
