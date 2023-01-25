from django.urls import path

from . import views


urlpatterns = [
    path("tag/<str:slug>/", views.TagDetails.as_view(), name="tag"),
    path("subscribe/<str:slug>/", views.subscribe, name="subscribe"),
    path("", views.TagList.as_view(), name="tags"),
]
