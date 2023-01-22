from notifications.models import Notification
from notifications import settings as notification_settings

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.views.generic import ListView
from notifications.utils import slug2id

from common import ajax_required, logging as log


class NotificationList(ListView):
    model = Notification
    context_object_name = "notifications"
    template_name = "actions/notifications.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(recipient=self.request.user)
            .order_by("-unread", "-timestamp")
        )


@log.logit_view
@require_GET
@login_required
@ajax_required
def mark_as_read(request):
    """This ajax view marks a notification as read.

    The request object is expected to have a GET parameter called 'slug'.
    """
    slug = request.GET.get("slug")
    notification_id = slug2id(slug)
    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id
    )
    notification.mark_as_read()
    return JsonResponse({"read": True})


@log.logit_view
@require_GET
@login_required
@ajax_required
def delete_notification(request):
    """This ajax view deletes a notification.

    The request object is expected to have a GET parameter called 'slug'.
    """
    slug = request.GET.get("slug")
    notification_id = slug2id(slug)
    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id
    )
    if notification_settings.get_config()["SOFT_DELETE"]:
        notification.deleted = True
        notification.save()
    else:
        notification.delete()
    return JsonResponse({"deleted": True})
