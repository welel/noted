from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.utils.translation import gettext_lazy as _

from .models import User


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if data.get("first_name") and data.get("last_name"):
            user.full_name = data["first_name"] + " " + data["last_name"]
        elif data.get("full_name"):
            user.full_name = data["full_name"]
        elif data.get("name"):
            user.full_name = data["name"]
        elif data.get("username"):
            user.full_name = data["username"]
        else:
            user.full_name = _("User Name")
        user.username = User.objects._generate_username(user.full_name)
        return user
