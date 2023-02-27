from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views


urlpatterns = [
    path(
        "signup-request/",
        views.SignupEmailView.as_view(),
        name="signup_request",
    ),
    path(
        "change-email-request/",
        views.ChangeemailEmailView.as_view(),
        name="change_email_request",
    ),
    path(
        "validate-email/",
        views.EmailExistanceCheckView.as_view(),
        name="validate_email",
    ),
    path(
        "validate-username/",
        views.UsernameExistanceCheckView.as_view(),
        name="validate_username",
    ),
    path(
        "change-email/<str:token>/",
        views.ChangeEmailView.as_view(),
        name="change_email",
    ),
    path(
        "delete-account/",
        views.DeleteUserView.as_view(),
        name="delete_account",
    ),
    path("signup/<str:token>/", views.SignupView.as_view(), name="signup"),
    path("signin/", views.SigninView.as_view(), name="signin"),
    path("signout/", LogoutView.as_view(), name="signout"),
    path("settings/", views.UpdateUserProfile.as_view(), name="settings"),
    path("follow/", views.FollowUserView.as_view(), name="follow"),
    path("task-status/", views.TaskStatusView.as_view(), name="task_status"),
    path(
        "switch-theme/", views.ThemeSwitcherView.as_view(), name="switch_theme"
    )
]
