from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.db import models
from django.db.models import Count, Q, QuerySet

from users.models import User


class SourceManager(models.Manager):
    def search(self, query: str) -> QuerySet:
        """Search source by `title` and return results."""
        similarity = TrigramSimilarity("title", query)
        return (
            self.annotate(similarity=similarity)
            .filter(similarity__gte=0.1)
            .order_by("-similarity")
        )


class NoteManager(models.Manager):
    def optimize(self):
        return self.prefetch_related(
            "author__profile",
            "source",
            "fork",
            "tags",
            "bookmarks",
            "likes",
        )

    def personal(self, user: User) -> QuerySet:
        """Query notes for a specific user (for private list).

        Args:
            user: An author of notes.

        Returns:
            Private notes for a specific user.
        """
        return self.filter(author=user)

    def profile(self, user: User) -> QuerySet:
        """Query notes for a specific user (for public list).

        Args:
            user: An author of notes.

        Returns:
            Public notes for a specific user.
        """
        return self.filter(author=user, draft=False, anonymous=False)

    def public(self) -> QuerySet:
        """Query public notes available for everyone."""
        return self.optimize().filter(draft=False)

    def by_created(self) -> QuerySet:
        """Query notes ordered by creation time (latest on the top)."""
        return self.optimize().order_by("-created")

    def with_source_type(self, type_code: str) -> QuerySet:
        """Query public notes with a specific source type."""
        return self.filter(draft=False, source__type=type_code)

    def popular(self) -> QuerySet:
        """Query public notes ordered by number of views."""
        return self.optimize().filter(draft=False).order_by("-views")

    def most_liked(self) -> QuerySet:
        """Query public notes ordered by number of likes."""
        return (
            self.optimize()
            .filter(draft=False)
            .annotate(count=Count("likes"))
            .order_by("-count")
        )

    def tags_in(self, tag_names: list) -> QuerySet:
        """Query public notes that have tags from `tag_names` list."""
        return (
            self.optimize()
            .filter(draft=False, tags__name__in=tag_names)
            .distinct()
        )

    def search(self, query: str) -> QuerySet:
        """Search public notes by `title`, `summary`, `body_raw`."""
        search_vector = (
            SearchVector("title", weight="A")
            + SearchVector("summary", weight="A")
            + SearchVector("body_raw", weight="B")
        )
        search_query = SearchQuery(query)
        headline = SearchHeadline(
            "title", search_query, start_sel="<mark>", stop_sel="</mark>"
        )
        return (
            self.filter(draft=False)
            .annotate(
                rank=SearchRank(search_vector, search_query),
                similarity=TrigramSimilarity("title", query),
                headline=headline,
            )
            .filter(Q(rank__gte=0.2) | Q(similarity__gt=0.1))
            .order_by("-rank")
        )
