from taggit.models import Tag

from django.db.models import Count, Q
from django.views.generic import ListView, DetailView

from content.models import Note


class TagList(ListView):
    """Display a annotated list of :model:`taggit.Tag`.

    It displays tags, each tag has a number of its' notes.

    TODO: Cache results.

    **Context**
        tags: a queryset of all :model:`taggit.Tag` instances.


    **Template**
        :template:`frontend/templates/tags/list.html`

    """

    model = Tag
    context_object_name = "tags"
    template_name = "tags/list.html"

    def get_queryset(self):
        queryset = Tag.objects.annotate(
            num_times=Count("notes", filter=Q(notes__private=False))
        ).filter(num_times__gt=0)
        return queryset


class TagDetails(DetailView):
    model = Tag
    template_name = "tags/tag_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notes"] = Note.objects.public().filter(
            tags__name__in=[self.get_object().name]
        )
        context["sidenotes"] = Note.objects.public()[:5]
        return context
