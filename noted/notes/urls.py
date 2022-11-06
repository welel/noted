from django.urls import path

from notes.views import (
    PublicNoteList,
    PersonalNoteList,
    NoteView,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView,
    TaggedNoteListView,
    UserNoteListView,
    notes_search,
)


urlpatterns = [
    path('', PublicNoteList.as_view(), name='home'),
    path('', PublicNoteList.as_view(), name='public_list'),
    path('personal/', PersonalNoteList.as_view(), name='personal'),
    path('view/<str:slug>/', NoteView.as_view(), name='note'),
    path('add/', NoteCreateView.as_view(), name='add'),
    path('update/<str:slug>/', NoteUpdateView.as_view(), name='update'),
    path('delete/<str:slug>/', NoteDeleteView.as_view(), name='delete'),
    path('tag/<str:tag_slug>/', TaggedNoteListView.as_view(), name='tagged'),
    path('user/<str:username>/', UserNoteListView.as_view(), name='by_user'),
    path('search/', notes_search, name='search'),
]
