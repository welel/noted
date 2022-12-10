from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.utils.translation import gettext_lazy as _

from users.models import User


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if "first_name" in data and "last_name" in data:
            user.full_name = data["first_name"] + " " + data["last_name"]
        elif "full_name" in data:
            user.full_name = data["full_name"]
        elif "name" in data:
            user.full_name = data["name"]
        elif "username" in data:
            user.full_name = data["username"]
        else:
            user.full_name = _("User Name")
        user.username = User.objects._generate_username(user.full_name)
        return user
