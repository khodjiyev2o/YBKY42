from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.rooms.models import Room


class RoomAvailabilityRetrieveView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        room = Room.objects.get(id=kwargs.get("pk"))
        date = self.request.query_params.get("date")
        availability = room.availability(date=date)
        return Response({"data": availability})


__all__ = ["RoomAvailabilityRetrieveView"]
