from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.utils.translation import gettext_lazy as _

from content.models import Note, Source
from common import ajax_required
from common import logging as log


class SourceDetailsView(log.LoggingView, DetailView):
    """A source details with list of notes of the source.

    **Context**
        notes: a note list of the current source.
        source_types: all source types of `Source`.
        sidenotes: a recommended note list.

    **Template**
        :template:`frontend/templates/content/source_display.html`

    """

    model = Source
    template_name = "content/source_display.html"

    @log.logit_class_method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notes"] = self.get_object().notes.filter(draft=False)
        context["source_types"] = dict(Source.TYPES)
        context["sidenotes"] = Note.objects.with_source_type(
            self.get_object().type
        )[:5]
        return context


class SourceTypeDetailsView(log.LoggingView, View):
    """A source type details with list of notes and sources of the source type.

    **Context**
        type_code: a code of a type.
        type: a readable type name.
        notes: a note list of the current source type.
        sources: a source list of the current source type.
        source_types: all source types of `Source`.
        sidenotes: a recommended note list.

    **Template**
        :template:`frontend/templates/content/source_type_details.html`

    """

    @log.logit_generic_view_request
    def get(self, request, code):
        try:
            type = Source.TYPES[int(code)]
        except (KeyError, ValueError):
            return HttpResponseBadRequest()
        context = {
            "type_code": type[0],
            "type": type[1],
            "notes": Note.objects.with_source_type(type[0]),
            "sources": Source.objects.filter(type=type[0]),
            "source_types": dict(Source.TYPES),
            "sidenotes": Note.objects.public()[:5],
        }
        return render(request, "content/source_type_details.html", context)


@log.logit_view
@ajax_required
def search_sources_select(request):
    """Search for sources by title and return JSON results.

    TODO: reduce given data and handle it in the template.
    """
    query = request.GET.get("query", "")
    data = Source.objects.search(query)
    data = [
        {
            "id": source.pk,
            "title": source.title,
            "type": [source.type, source.verbose_type],
            "link": source.link,
            "description": source.description,
        }
        for source in data
    ]
    return JsonResponse({"data": data}, status=200)
