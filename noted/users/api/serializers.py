from rest_framework import serializers

from common.helpers import get_absolute_uri

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField()

    def get_profile_url(self, user):
        return get_absolute_uri(user.profile.get_absolute_url())

    class Meta:
        model = User
        fields = ("id", "username", "full_name", "profile_url")
