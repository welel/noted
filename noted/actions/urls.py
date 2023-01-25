from django.urls import path

from . import views


urlpatterns = [
    path(
        "notifications/",
        views.NotificationList.as_view(),
        name="notifications",
    ),
    path("notice/read/", views.mark_as_read, name="mark_as_read"),
    path(
        "notice/delete/", views.delete_notification, name="delete_notification"
    ),
]
