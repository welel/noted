from django.views.generic.detail import DetailView
from django.urls import path

from content import views
from content.models import Note


urlpatterns = [
    path("", views.PublicNoteList.as_view(), name="home"),
    path("add-note/", views.NoteCreateView.as_view(), name="create_note"),
    path(
        "edit-note/<str:slug>/",
        views.NoteUpdateView.as_view(),
        name="edit_note",
    ),
    path(
        "del-note/<str:slug>/",
        views.NoteDeleteView.as_view(),
        name="delete_note",
    ),
    path("note/<str:slug>/", views.NoteView.as_view(), name="note"),
    path(
        "search-sources-select",
        views.search_sources_select,
        name="search_sources_select",
    )
    # path("source/<str:slug>/", _, name="source"),
]
