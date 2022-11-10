from django.urls import path

from user.views import edit_user, profile


urlpatterns = [
    path('edit', edit_user, name='edit_user'),
    path('profile/<str:username>', profile, name='user_profile'),
]
