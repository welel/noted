from django.urls import path

from . import views


urlpatterns = [
    path("", views.PublicNoteList.as_view(), name="home"),
    path("welcome/", views.WelcomeNoteList.as_view(), name="welcome"),
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
    path("note/fork/<str:slug>/", views.NoteForkView.as_view(), name="fork"),
    path("note/pin/<str:slug>/", views.pin_note, name="pin_note"),
    path("note/like/<str:slug>/", views.like_note, name="like_note"),
    path(
        "note/bookmark/<str:slug>/", views.bookmark_note, name="bookmark_note"
    ),
    path(
        "note/download/<str:filetype>/<str:slug>/",
        views.download_note,
        name="download_note",
    ),
    path(
        "u/notes/<str:slug>/",
        views.ProfileNoteList.as_view(),
        name="profile_notes",
    ),
    path("p/notes/", views.PersonalNotesView.as_view(), name="personal_notes"),
    path("search/<str:type>/", views.search, name="search"),
    path(
        "source/search/",
        views.search_sources_select,
        name="search_sources_select",
    ),
    path(
        "source/<str:slug>/", views.SourceDetailsView.as_view(), name="source"
    ),
    path(
        "source/type/<str:code>/",
        views.SourceTypeDetailsView.as_view(),
        name="source_type",
    ),
]
