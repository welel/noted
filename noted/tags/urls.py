from django.urls import path

from tags.views import TagList


urlpatterns = [
    path('', TagList.as_view(), name='tags'),
]
