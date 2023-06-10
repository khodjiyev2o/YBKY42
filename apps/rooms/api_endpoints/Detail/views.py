from rest_framework.generics import RetrieveAPIView

from apps.rooms.api_endpoints.Detail.serializers import RoomDetailSerializer
from apps.rooms.models import Room


class RoomDetailView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer


__all__ = ["RoomDetailView"]
