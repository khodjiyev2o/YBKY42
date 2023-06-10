from rest_framework import serializers

from apps.rooms.models import Room


class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "name", "type", "capacity")
