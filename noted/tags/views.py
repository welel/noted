from taggit.models import Tag

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from content.models import Note
from common import ajax_required
from common.logging import LoggingView, logging_view


class TagList(LoggingView, ListView):
    """Display a annotated list of :model:`taggit.Tag`.

    It displays tags, each tag has a number of its' notes.

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


class TagDetails(LoggingView, DetailView):
    """Tag details with a list of notes of the current tag."""

    model = Tag
    template_name = "tags/tag_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notes"] = Note.objects.public().filter(
            tags__name__in=[self.get_object().name]
        )
        context["sidenotes"] = Note.objects.public()[:5]
        return context


@logging_view
@require_GET
@login_required(login_url=reverse_lazy("account_login"))
@ajax_required
def subscribe(request, slug):
    """Starts/ends following a tag."""
    tag = get_object_or_404(Tag, slug=slug)
    if tag in request.user.tags.all():
        request.user.tags.remove(tag.name)
        return JsonResponse({"result": "removed"})
    else:
        request.user.tags.add(tag.name)
        return JsonResponse({"result": "added"})
