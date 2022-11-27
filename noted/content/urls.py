from django.urls import path

from content import views


urlpatterns = [
    # path("source-type/<str:slug>/", _, name="source_type"),
    # path("source/<str:slug>/", _, name="source"),
    path("", views.home, name="home"),
]
