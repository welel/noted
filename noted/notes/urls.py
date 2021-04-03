from django.urls import path

from notes.views import NoteList, NoteDetailView, NoteCreateView


urlpatterns = [
    path('', NoteList.as_view(), name='home'),
    path('add/', NoteCreateView.as_view(), name='add'),
    path('note/<str:slug>/', NoteDetailView.as_view(), name='note'),
]
