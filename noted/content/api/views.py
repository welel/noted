from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User

from ..models import Note, Source
from .serializers import SourceSerializer, PublicNoteSerializer, NoteSerializer


class PublicNoteViewSet(ModelViewSet):
    queryset = Note.objects.filter(draft=False).order_by("-created")
    serializer_class = PublicNoteSerializer
    permission_classes = [permissions.AllowAny]


class NoteDetailAPIView(RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def retrieve(self, request, *args, **kwargs):
        note = self.get_object()
        if note.draft and note.author != request.user:
            return Response({"detail": "Invalid token."}, status=401)
        serializer = self.get_serializer(note)
        return Response(serializer.data)


class ProfileNoteAPIView(APIView):
    def get_queryset(self):
        return Note.objects.filter(draft=False)

    def get(self, request, id: int, *args, **kwargs):
        if not User.objects.filter(id=id).exists():
            return Response({"detail": f"No users with id {id}."}, status=404)
        queryset = self.get_queryset().filter(author__id=id)
        data = NoteSerializer(queryset, many=True).data
        return Response(data)


class PersonalNoteAPIView(APIView):
    def get_queryset(self):
        return Note.objects.all()

    def get(self, request, *args, **kwargs):
        if not request.auth:
            return Response({"detail": f"Invalid token."}, status=401)
        queryset = self.get_queryset().filter(author=request.user)
        data = NoteSerializer(queryset, many=True).data
        return Response(data)


class SourceViewSet(ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = [permissions.AllowAny]


class SourceDetailView(RetrieveAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
