from rest_framework.response import Response
from rest_framework.views import APIView

from apps.rooms.models import Room


class RoomAvailabilityRetrieveView(APIView):
    def get(self, request, *args, **kwargs):
        room = Room.objects.get(id=kwargs.get("pk"))
        date = self.request.query_params.get("date")
        availability = room.availability(date=date)
        return Response(availability)


__all__ = ["RoomAvailabilityRetrieveView"]
