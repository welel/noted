from django.urls import path

from notes.views import (
    NoteList,
    PersonalNoteList,
    NoteDetailView,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView,
    TaggedNoteListView,
    TagList,
    UserNoteListView,
)


urlpatterns = [
    path('', NoteList.as_view(), name='home'),
    path('personal/', PersonalNoteList.as_view(), name='personal'),
    path('view/<str:slug>/', NoteDetailView.as_view(), name='note'),
    path('add/', NoteCreateView.as_view(), name='add'),
    path('update/<str:slug>/', NoteUpdateView.as_view(), name='update'),
    path('delete/<str:slug>/', NoteDeleteView.as_view(), name='delete'),
    path('tags/', TagList.as_view(), name='tags'),
    path('tag/<str:tag_slug>/', TaggedNoteListView.as_view(), name='tagged'),
    path('user/<str:username>/', UserNoteListView.as_view(), name='by_user'),
]
