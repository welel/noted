from django.db.models import Count
from django.views.generic import ListView

from taggit.models import Tag


class TagList(ListView):
    model = Tag
    context_object_name = 'tags'
    template_name = 'tags/list.html'

    def get_queryset(self):
        queryset = Tag.objects.all()
        qs_counted = queryset.annotate(
            num_times=Count('taggit_taggeditem_items')
        )
        return qs_counted.order_by('-num_times')
