from django import template
from django.utils.safestring import mark_safe

from content.models import Source


register = template.Library()

# HTML template for bootstrap icon for a source type
ICON_TEMPLATE = '<i class="bi {icon}" style="font-size: {size}; \
    background-color: rgba({rgb},{bg_alpha});  padding: 4px 10px 4px 10px; \
    border-radius: 50px;" data-bs-toggle="tooltip" \
    data-bs-title="{tooltip}"></i>'

# Data mapping for `ICON_TEMPLATE`
SOURCE_ICONS = {
    Source.DEFAULT: {"icon": "bi-grid", "color": "213, 213, 213"},
    Source.BOOK: {"icon": "bi-book", "color": "200, 93, 93"},
    Source.COURSE: {"icon": "bi-mortarboard-fill", "color": "107, 234, 139"},
    Source.VIDEO: {"icon": "bi-camera-video", "color": "150, 200, 255"},
    Source.ARTICLE: {"icon": "bi-journal-richtext", "color": "185, 143, 227"},
    Source.LECTURE: {"icon": "bi-pen", "color": "100, 235, 255"},
    Source.TUTORIAL: {"icon": "bi-map", "color": "232, 222, 76"},
}


@register.filter
def icon(source_code, size: str = "1rem", background_alpha: str = "1"):
    """Transform `source_code` to HTML icon of a source."""
    if source_code not in SOURCE_ICONS:
        return ""
    icon = ICON_TEMPLATE.format(
        icon=SOURCE_ICONS[source_code]["icon"],
        size=size,
        rgb=SOURCE_ICONS[source_code]["color"],
        bg_alpha=background_alpha,
        tooltip=Source.make_type_readable(source_code),
    )
    return mark_safe(icon)


@register.filter
def readabletype(source_code: str):
    """Transform `source_code` to a human readable source name."""
    if source_code not in [s[0] for s in Source.TYPES]:
        return ""
    return Source.make_type_readable(source_code)
