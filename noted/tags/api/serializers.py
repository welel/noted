"""Content API endpoints.

API table
| Endpoint    | Method | Result                                   |
| ----------- | ------ | ---------------------------------------- |
| notes/      | GET    | list of public notes                     |
| note/id/    | GET    | a note (API restriction)                 |
| profile/id/ | GET    | list of public notes of some user        |
| personal/   | GET    | list of personal notes (API restriction) |
| sources/    | GET    | list of sources                          |
| source/id/  | GET    | a source                                 |

"""

from rest_framework import serializers

from common.helpers import get_absolute_uri

from ..models import UnicodeTag


class TagSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, tag):
        return get_absolute_uri(tag.get_absolute_url())

    class Meta:
        model = UnicodeTag
        exclude = ("slug",)
