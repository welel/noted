import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    FormView,
)
from django.views.generic.edit import DeleteView
from django.views import View

from content.forms import NoteForm
from content.models import Note, Source


def home(request):
    notes = Note.objects.all()
    source_types = dict(Source.TYPES)
    context = {"notes": notes, "source_types": source_types}
    return render(request, "index.html", context)


def search_sources_select(request):
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


class NoteDetailsView(DetailView):
    model = Note
    template_name = "content/note_display.html"
