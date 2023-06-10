from django.core.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.rooms.api_endpoints.Booking.serializers import BookingCreateSerializer
from apps.rooms.exceptions import InvalidTimeError
from apps.rooms.models import Room


class CreateBookingView(GenericAPIView):
    """Send time in this format: YYYY-MM-DD hh:mm:ss"""
    serializer_class = BookingCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            room = Room.objects.get(id=kwargs.get("pk"))
        except Room.DoesNotExist:
            return Response({"error": "Xona mavjud emas"}, status=404)

        try:
            self.perform_create(serializer=serializer, room=room)
        except ValidationError:
            return Response({"error": "uzr, siz tanlagan vaqtda xona band"}, status=404)
        except InvalidTimeError:
            return Response({"error": "Notugri vaqt"}, status=404)

        return Response({"message": "xona muvaffaqiyatli band qilindi"})

    def perform_create(self, serializer, room):
        serializer.save(room=room)


__all__ = ["CreateBookingView"]
