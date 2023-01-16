from notifications.models import Notification

from django.views.generic import ListView


class NotificationList(ListView):
    model = Notification
    context_object_name = "notifications"
    template_name = "actions/notifications.html"
