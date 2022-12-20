from taggit.models import Tag

from django.contrib.postgres.search import TrigramSimilarity, SearchVector
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from content.models import Note, Source
from users.models import User


def search(request, type):
    """Search by notes, sources, tags, users."""
    query = request.GET.get("query")
    context = {"query": query, "type": type}

    if type == "notes":
        context["notes"] = Note.objects.search(query)

    elif type == "sources":
        context["sources"] = Source.objects.search(query)

    elif type == "tags":
        similarity = TrigramSimilarity("name", query)
        context["tags"] = (
            Tag.objects.annotate(similarity=similarity)
            .filter(similarity__gte=0.1)
            .order_by("-similarity")
        )

    elif type == "people":
        vector = SearchVector("full_name", "username")
        context["users"] = User.objects.annotate(search=vector).filter(
            search=query
        )

    return render(request, "content/search.html", context)
