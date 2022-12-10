from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.views.generic.edit import DeleteView
from django.views import View
from django.utils.translation import gettext_lazy as _

from content.forms import NoteForm
from content.models import Note, Source
from common import ajax_required


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
    paginate_by = 18

    def get_ordering(self):
        return self.request.GET.get("order", default="-datetime_created")

    def get_ordered_queryset(self):
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
        # add More from NoteD.
        return context


@ajax_required
def search_sources_select(request):
    """Search for sources by title and return JSON results."""
    query = request.GET.get("query", "[{]}(2")
    data = Source.objects.filter(title__icontains=query)
    data = [
        {
            "id": source.pk,
            "title": source.title,
            "type": [source.type, source.get_readable_type()],
        }
        for source in data
    ]
    return JsonResponse({"data": data}, status=200)


@method_decorator(login_required, name="dispatch")
class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = "content/note_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class NoteUpdateView(UpdateView):
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
        context["notes"] = Note.objects.public()[:5]
        return context


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
