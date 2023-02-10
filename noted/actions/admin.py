from notifications.admin import NotificationAdmin
from notifications.models import Notification

from django.contrib import admin

from .models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("actor", "verb", "target", "created")
    list_filter = ("created", "verb", "target_ct")
    search_fields = ("verb",)


class NewNotificationAdmin(NotificationAdmin):
    list_display = ("actor", "verb", "target", "recipient", "unread", "public")
    list_filter = ("verb", "level", "unread", "public", "timestamp")


admin.site.unregister(Notification)
admin.site.register(Notification, NewNotificationAdmin)
