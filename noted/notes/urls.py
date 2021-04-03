from django.urls import path

from notes.views import NoteList


urlpatterns = [
    path('', NoteList.as_view(), name='home'),
]
