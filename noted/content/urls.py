from django.views.generic.detail import DetailView
from django.urls import path

from content import views
from content.models import Note


urlpatterns = [
    path("", views.home, name="home"),
    path("add-note/", views.create_note, name="create_note"),
    path(
        "note/<str:slug>/",
        DetailView.as_view(
            model=Note, template_name="content/note_display.html"
        ),
        name="note",
    ),
    # path("source-type/<str:slug>/", _, name="source_type"),
    # path("source/<str:slug>/", _, name="source"),
]
