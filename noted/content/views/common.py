import logging

from taggit.models import Tag

from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page

from content.models import Note, Source
from users.models import User


logger = logging.getLogger("django.request")


@cache_page(60 * 3)
def search(request, type: str):
    """Search by notes, sources, tags, users.

    Args:
        type: A type of searching (notes/sources/tags/people).
    """
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

    else:
        logger.warning(
            f"Bad search request {type} not in [notes, sources, tags, people]"
        )

    return render(request, "content/search.html", context)
