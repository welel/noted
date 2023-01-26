from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ModelViewSet

from ..models import UnicodeTag
from .serializers import TagSerializer


class TagViewSet(ModelViewSet):
    queryset = UnicodeTag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class TagDetailView(RetrieveAPIView):
    queryset = UnicodeTag.objects.all()
    serializer_class = TagSerializer
