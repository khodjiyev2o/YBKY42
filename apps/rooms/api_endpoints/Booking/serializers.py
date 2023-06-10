from rest_framework import serializers

from apps.rooms.models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("resident", "start_time", "end_time")
