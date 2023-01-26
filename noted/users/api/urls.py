from django.urls import path

from . import views


urlpatterns = [
    path("users/", views.UserViewSet.as_view({"get": "list"}), name="users"),
    path("user/<int:pk>/", views.UserDetailView.as_view(), name="user"),
]
