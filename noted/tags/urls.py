from django.urls import path

from tags import views


urlpatterns = [
    path("tag/<str:slug>/", views.TagDetails.as_view(), name="tag"),
    path("", views.TagList.as_view(), name="tags"),
]
