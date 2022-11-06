from django.db.models import Count
from django.views.generic import ListView

from taggit.models import Tag


class TagList(ListView):
    """Display a annotated list of :model:`taggit.Tag`.

    It displays tags, each tag has a number of his notes.

    TODO: exclude `private`=True notes from tag counting.

    **Context**
        tags: a queryset of all :model:`taggit.Tag` instances.


    **Template**
        :template:`frontend/templates/tags/list.html`

    """
    model = Tag
    context_object_name = 'tags'
    template_name = 'tags/list.html'

    def get_queryset(self):
        queryset = Tag.objects.all().annotate(
            num_times=Count('taggit_taggeditem_items')
        )
        # If a tag has no notes, we delete the tag.
        for tag in reversed(queryset):
            if tag.num_times == 0:
                tag.delete()
        return queryset.order_by('-num_times')
