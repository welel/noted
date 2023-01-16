from django.urls import path

from actions import views


urlpatterns = [
    path(
        "notifications/",
        views.NotificationList.as_view(),
        name="notifications",
    ),
]
