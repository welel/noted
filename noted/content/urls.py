from django.urls import path

from content import views


urlpatterns = [
    path('', views.home, name='home')
]
