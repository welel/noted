from django.urls import path

from notes.views import (
    NoteList,
    NoteDetailView,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView,
)


urlpatterns = [
    path('', NoteList.as_view(), name='home'),
    path('view/<str:slug>/', NoteDetailView.as_view(), name='note'),
    path('add/', NoteCreateView.as_view(), name='add'),
    path('update/<str:slug>/', NoteUpdateView.as_view(), name='update'),
    path('delete/<str:slug>/', NoteDeleteView.as_view(), name='delete'),
]