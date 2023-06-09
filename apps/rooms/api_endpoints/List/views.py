from rest_framework.generics import ListAPIView

from apps.rooms.api_endpoints.List.serializers import RoomListSerializer
from apps.rooms.models import Room


class RoomListView(ListAPIView):
    queryset = Room.objects.filter()
    serializer_class = RoomListSerializer
    search_fields = ("name",)
    filterset_fields = ("type",)


__all__ = ["RoomListView"]
