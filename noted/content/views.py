from django.contrib.auth.decorators import login_required
from django.db.models import F, QuerySet
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.views.generic.edit import DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

from content.forms import NoteForm
from content.models import Note, Source
from content.search import search_sources
from common import ajax_required
from users.models import User


class NoteList(ListView):
    """Display a list of :model:`notes.Note`.

    Uses as a superclass for other specific notes listings.

    Notes order options (provides through a GET param `order`):
        `datetime_created`: from oldest to newest by publish date.
        `-datetime_created`: from newest to oldest by publish date.

    **Context**
        notes: a queryset of :model:`notes.Note` instances.
        paginator: a paginator for notes list.
        page_obj: a pagination navigator.
        order_label: a human readable label of a notes order option.
    """

    ORDER_LABELS = {
        "datetime_created": _("Oldest"),
        "-datetime_created": _("Latest"),
    }
    SORTING_FUNCS_MAPPING = {
        "datetime_created": Note.objects.datetime_created,
        "-datetime_created": Note.objects.datetime_created_dec,
    }

    model = Note
    context_object_name = "notes"
    paginate_by = 100

    def get_ordering(self) -> str:
        return self.request.GET.get("order", default="-datetime_created")

    def get_ordered_queryset(self) -> QuerySet:
        """Order a queryset by GET param `order`."""
        order = self.get_ordering()
        return self.SORTING_FUNCS_MAPPING[order]()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_ordering()
        context["order_label"] = self.ORDER_LABELS.get(order, "")
        return context


class PublicNoteList(NoteList):
    """Display a list of :model:`notes.Note` available for every one.

    It displays the home page of the website. A list consists of all notes
    except drafts.

    **Context**
        notes: a queryset of :model:`notes.Note` instances.
        paginator: a paginator for notes list.
        page_obj: a pagination navigator.
        order_label: a human readable label of a notes order option.
        source_types: all source types.

    **Template**
        :template:`frontend/templates/index.html`
    """

    template_name = "index.html"

    def get_queryset(self):
        return super().get_ordered_queryset().filter(draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["source_types"] = dict(Source.TYPES)
        context["sidenotes"] = Note.objects.public()[:5]
        return context


class ProfileNoteList(NoteList):
    """Display a list of public :model:`notes.Note` of a selected user."""

    template_name = "content/note_list_profile.html"

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get("user_pk"))
        return (
            super()
            .get_ordered_queryset()
            .filter(author=user, draft=False, anonymous=False)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("user_pk")
        context["user"] = get_object_or_404(User, pk=pk)
        context["pins"] = self.get_queryset().filter(pin=True)
        context["sidenotes"] = Note.objects.public()[:5]
        return context


class NoteDraftMixin:
    def form_valid(self, form):
        form.instance.draft = self.draft
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.draft = "savedraft" in request.POST
        return super().post(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class NoteCreateView(NoteDraftMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "content/note_create.html"

    def get_initial(self):
        initial = super().get_initial()
        try:
            source = Source.objects.get(slug=self.request.GET.get("source"))
        except Source.DoesNotExist:
            return initial
        initial["source"] = source.title
        initial["source_type"] = source.type
        initial["source_link"] = source.link
        initial["source_description"] = source.description
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class NoteForkView(NoteCreateView):
    def get_initial(self):
        initial = super().get_initial()
        try:
            note = Note.objects.get(slug=self.kwargs.get("slug"))
        except Source.DoesNotExist:
            return initial
        note.fork = Note.objects.get(pk=note.pk)
        note.pk = None
        note.slug = None
        self.object = note
        if note.source:
            initial["source"] = note.source.title
            initial["source_type"] = note.source.type
            initial["source_link"] = note.source.link
            initial["source_description"] = note.source.description
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
    model = Note
    template_name = "content/note_display.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidenotes"] = Note.objects.public()[:5]
        return context

    def get_object(self):
        note = super().get_object()
        if note:
            Note.objects.filter(pk=note.pk).update(views=F("views") + 1)
        return note


class NoteView(View):
    """Chose a view based on a request method (GET/POST).

    It uses two different class based views with the same URL. We have
    a division here: GET requests should get the ``NoteDetailView`` (with
    a form added to the context data), and POST requests should get
    the ``CommentFormView``.
    """

    def get(self, request, *args, **kwargs):
        view = NoteDetailsView.as_view()
        return view(request, *args, **kwargs)

    # For future (comments)
    # def post(self, request, *args, **kwargs):
    #     view = CommentFormView.as_view()
    #     return view(request, *args, **kwargs)


@require_GET
@login_required(login_url=reverse_lazy("account_login"))
@ajax_required
def pin_note(request, slug):
    note = get_object_or_404(Note, slug=slug)
    if note.author != request.user:
        return HttpResponseBadRequest()
    note.pin = not note.pin
    note.save()
    return JsonResponse({"pin": note.pin})


@require_GET
@login_required(login_url=reverse_lazy("account_login"))
@ajax_required
def like_note(request, slug):
    note = get_object_or_404(Note, slug=slug)
    if request.user in note.likes.all():
        note.likes.remove(request.user)
        return JsonResponse({"liked": False})
    else:
        note.likes.add(request.user)
        return JsonResponse({"liked": True})


@require_GET
@login_required(login_url=reverse_lazy("account_login"))
@ajax_required
def bookmark_note(request, slug):
    note = get_object_or_404(Note, slug=slug)
    if request.user in note.bookmarks.all():
        note.bookmarks.remove(request.user)
        return JsonResponse({"bookmarked": False})
    else:
        note.bookmarks.add(request.user)
        return JsonResponse({"bookmarked": True})


from wsgiref.util import FileWrapper
from django.http import HttpResponse


@require_GET
@login_required(login_url=reverse_lazy("account_login"))
def download_note(request, filetype: str, slug: str):
    note = get_object_or_404(Note, slug=slug)
    file = note.generate_file_to_response(filetype=filetype)
    if not file or (note.draft and request.user != note.author):
        return HttpResponseBadRequest()
    response = HttpResponse(
        FileWrapper(file["file"]), content_type=file["content_type"]
    )
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{file["filename"]}"'.encode(encoding="utf-8")
    return response


class SourceDetailsView(DetailView):
    model = Source
    template_name = "content/source_display.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notes"] = self.get_object().notes.all().filter(draft=False)
        context["source_types"] = dict(Source.TYPES)
        context["sidenotes"] = Note.objects.by_source_type(
            self.get_object().type
        )[:5]
        return context


class SourceTypeDetailsView(View):
    def get(self, request, code):
        context = {}
        try:
            type = Source.TYPES[int(code)]
        except (KeyError, ValueError):
            return HttpResponseBadRequest()
        context["type_code"] = type[0]
        context["type"] = type[1]
        context["notes"] = Note.objects.by_source_type(type[0])
        context["sources"] = Source.objects.by_type(type[0])
        context["source_types"] = dict(Source.TYPES)
        context["sidenotes"] = Note.objects.public()[:5]
        return render(request, "content/source_type_details.html", context)


@ajax_required
def search_sources_select(request):
    """Search for sources by title and return JSON results."""
    query = request.GET.get("query", "")
    data = search_sources(query)
    data = [
        {
            "id": source.pk,
            "title": source.title,
            "type": [source.type, source.get_readable_type()],
            "link": source.link,
            "description": source.description,
        }
        for source in data
    ]
    return JsonResponse({"data": data}, status=200)


def search(request, type):
    query = request.GET.get("query")
    context = {"query": query, "type": type}

    if type == "notes":
        context["notes"] = {}

    elif type == "sources":
        context["sources"] = search_sources(query)

    return render(request, "content/search.html", context)
