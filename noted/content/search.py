from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet

from content.models import Source


def search_sources(query: str) -> QuerySet:
    similarity = TrigramSimilarity("title", query)
    return (
        Source.objects.annotate(similarity=similarity)
        .filter(similarity__gte=0.1)
        .order_by("-similarity")
    )
