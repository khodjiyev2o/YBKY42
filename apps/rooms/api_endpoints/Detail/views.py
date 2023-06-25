from rest_framework.generics import RetrieveAPIView

from apps.rooms.api_endpoints.Detail.serializers import RoomDetailSerializer
from apps.rooms.models import Room
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


class RoomDetailView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer

    def get(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(id=self.kwargs.get('pk'))
        except Room.DoesNotExist:

            return Response({"error": "topilmadi"}, status=404)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


__all__ = ["RoomDetailView"]
