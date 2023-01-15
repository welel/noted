from taggit.models import Tag

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from actions.models import Action
from content.models import Note
from common import ajax_required
from common import logging as log


class TagList(log.LoggingView, ListView):
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

    @log.logit_class_method
    def get_queryset(self):
        queryset = Tag.objects.annotate(
            num_times=Count("notes", filter=Q(notes__private=False))
        ).filter(num_times__gt=0)
        return queryset


class TagDetails(log.LoggingView, DetailView):
    """Tag details with a list of notes of the current tag.

    **Context**
        sidenotes: suggested notes on a sidebar.
        notes: a queryset of notes of the current tag.

    **Template**
        :template:`frontend/templates/tags/tag_details.html`

    """

    model = Tag
    template_name = "tags/tag_details.html"

    @log.logit_class_method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notes"] = Note.objects.public().filter(
            tags__name__in=[self.get_object().name]
        )
        context["sidenotes"] = Note.objects.public()[:5]
        return context


@log.logit_view
@require_GET
@login_required(login_url=reverse_lazy("account_login"))
@ajax_required
def subscribe(request, slug):
    """Starts/ends following a tag."""
    tag = get_object_or_404(Tag, slug=slug)
    if tag in request.user.profile.tags.all():
        request.user.profile.tags.remove(tag.name)
        return JsonResponse({"result": "removed"})
    else:
        request.user.profile.tags.add(tag.name)
        Action.objects.create_action(request.user, Action.FOLLOW_TAG, tag)
        return JsonResponse({"result": "added"})
