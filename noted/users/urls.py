from django.urls import path

from . import views


urlpatterns = [
    path("signup-request/", views.send_singup_email, name="signup_request"),
    path(
        "change-email-request/",
        views.send_change_email,
        name="change_email_request",
    ),
    path("change-email/<str:token>/", views.change_email, name="change_email"),
    path("validate-email/", views.validate_email, name="validate_email"),
    path(
        "validate-username/", views.validate_username, name="validate_username"
    ),
    path("signup/<str:token>/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("settings/", views.UpdateUserProfile.as_view(), name="settings"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("follow/", views.user_follow, name="follow"),
]
