from django.urls import path

from . import views


urlpatterns = [
    path(
        "notes/",
        views.PublicNoteViewSet.as_view({"get": "list"}),
        name="notes",
    ),
    path(
        "note/<int:pk>/",
        views.NoteDetailAPIView.as_view(),
        name="note",
    ),
    path(
        "profile/<int:id>/",
        views.ProfileNoteAPIView.as_view(),
        name="profile",
    ),
    path(
        "personal/",
        views.PersonalNoteAPIView.as_view(),
        name="personal",
    ),
    path(
        "sources/",
        views.SourceViewSet.as_view({"get": "list"}),
        name="sources",
    ),
    path("source/<int:pk>/", views.SourceDetailView.as_view(), name="source"),
]
