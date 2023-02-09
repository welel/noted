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
    path("signup/<str:token>/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("settings/", views.UpdateUserProfile.as_view(), name="settings"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("follow/", views.user_follow, name="follow"),
]
