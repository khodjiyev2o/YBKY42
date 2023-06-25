from rest_framework import serializers

from apps.rooms.models import Booking
from django.conf import settings
from apps.users.models import User


class ResidentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = ('name',)


class BookingCreateSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS)
    end = serializers.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS)
    resident = ResidentSerializer()

    class Meta:
        model = Booking
        fields = ("resident", "start", "end")

    def create(self, validated_data):
        resident_data = validated_data.pop('resident')
        booking = Booking.objects.create(resident=resident_data['first_name'], **validated_data)

        return booking
