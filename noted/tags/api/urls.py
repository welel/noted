from django.urls import path

from . import views


urlpatterns = [
    path("tags/", views.TagViewSet.as_view({"get": "list"}), name="tags"),
    path("tag/<int:pk>/", views.TagDetailView.as_view(), name="tag"),
]
