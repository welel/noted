from django.urls import path

from content import views


urlpatterns = [
    path("", views.PublicNoteList.as_view(), name="home"),
    path("note/add/", views.NoteCreateView.as_view(), name="create_note"),
    path(
        "note/edit/<str:slug>/",
        views.NoteUpdateView.as_view(),
        name="edit_note",
    ),
    path(
        "note/delete/<str:slug>/",
        views.NoteDeleteView.as_view(),
        name="delete_note",
    ),
    path("note/<str:slug>/", views.NoteView.as_view(), name="note"),
    path(
        "source/search/",
        views.search_sources_select,
        name="search_sources_select",
    )
    # path("source/<str:slug>/", _, name="source"),
]
