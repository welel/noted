from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView

from common import logging as log
from common.decorators import ajax_required
from content.models import Note, Source


class SourceDetailsView(DetailView):
    """A source details with list of notes of the source.

    **Context**
        notes: A note list of the current source.
        source_types: All source types of `Source`.
        sidenotes: A recommended note list.

    **Template**
        :template:`frontend/templates/content/source_display.html`

    """

    model = Source
    template_name = "content/source_display.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notes"] = self.get_object().notes.filter(draft=False)
        context["source_types"] = dict(Source.TYPES)
        context["sidenotes"] = Note.objects.with_source_type(
            self.get_object().type
        )[:5]
        return context


class SourceTypeDetailsView(View):
    """A source type details with list of notes and sources of the source type.

    **Context**
        type_code: A code of a type.
        type: A readable type name.
        notes: A note list of the current source type.
        sources: A source list of the current source type.
        source_types: All source types of `Source`.
        sidenotes: A recommended note list.

    **Template**
        :template:`frontend/templates/content/source_type_details.html`

    """

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


@ajax_required()
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
