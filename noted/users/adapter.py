from django.utils.translation import gettext_lazy as _

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from common.logging import logit_generic_view_request

from .models import User


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    @logit_generic_view_request
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if (
            "first_name" in data
            and "last_name" in data
            and data["first_name"]
            and data["last_name"]
        ):
            user.full_name = data["first_name"] + " " + data["last_name"]
        elif "full_name" in data and data["full_name"]:
            user.full_name = data["full_name"]
        elif "name" in data and data["name"]:
            user.full_name = data["name"]
        elif "username" in data and data["username"]:
            user.full_name = data["username"]
        else:
            user.full_name = _("User Name")
        user.username = User.objects._generate_username(user.full_name)
        return user
