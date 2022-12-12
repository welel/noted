from django import template
from django.utils.safestring import mark_safe

from content.models import Source


register = template.Library()


SOURCE_ICONS = {
    Source.DEFAULT: '<i class="bi bi-grid" style="font-size: %s;"></i>',
    Source.BOOK: '<i class="bi bi-book" style="font-size: %s;"></i>',
    Source.ARTICLE: '<i class="bi bi-journal-richtext" style="font-size: %s;"></i>',
    Source.COURSE: '<i class="bi bi-mortarboard-fill" style="font-size: %s;"></i>',
    Source.LECTURE: '<i class="bi bi-pen" style="font-size: %s;"></i>',
    Source.TUTORIAL: '<i class="bi bi-map" style="font-size: %s;"></i>',
    Source.VIDEO: '<i class="bi bi-camera-video" style="font-size: %s;"></i>',
}


@register.filter
def icon(source_code, size="1rem"):
    """Transform `source_code` to HTML icon of a source."""
    if source_code not in SOURCE_ICONS:
        return ""
    return mark_safe(SOURCE_ICONS[source_code] % size)


@register.filter
def readabletype(source_code):
    """Transform `source_code` to a human readable source name."""
    if source_code not in [s[0] for s in Source.TYPES]:
        return ""
    return Source.make_type_readable(source_code)
