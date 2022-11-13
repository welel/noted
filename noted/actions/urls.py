from django.urls import path

from actions.views import feed, note_feed


urlpatterns = [
    #path('feed/', feed, name='feed'),
    path('note-feed/', note_feed, name='note_feed'),
]
