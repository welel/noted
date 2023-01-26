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
from tags.api.serializers import TagSerializer
from users.api.serializers import UserSerializer

from ..models import Note, Source


class SourceSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_url(self, source):
        return get_absolute_uri(source.get_absolute_url())

    def get_type(self, source):
        return source.verbose_type

    class Meta:
        model = Source
        exclude = ("slug",)


class NoteSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    author = UserSerializer()
    source = SourceSerializer()
    tags = TagSerializer(many=True)

    def get_url(self, note):
        return get_absolute_uri(note.get_absolute_url())

    def get_language(self, note):
        return {"ru": "Russian", "en": "English", "er": "Undetected"}[
            note.lang
        ]

    def get_likes(self, note):
        return note.likes.count()

    class Meta:
        model = Note
        exclude = ("body_html", "bookmarks", "slug", "lang", "anonymous")


class PublicNoteSerializer(NoteSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, note):
        return None if note.anonymous else UserSerializer(note.author).data
