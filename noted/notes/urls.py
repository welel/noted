from django.urls import path

from notes.views import NoteList, NoteDetailView


urlpatterns = [
    path('', NoteList.as_view(), name='home'),
    path('<str:slug>/', NoteDetailView.as_view(), name='note'),
]
