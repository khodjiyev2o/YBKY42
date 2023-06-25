from django.urls import reverse
from rest_framework.test import APITestCase

from apps.rooms.models import Room, RoomType


class TestRoomDetailView(APITestCase):
    def setUp(self):
        self.team_room = Room.objects.create(name="workly", type=RoomType.TEAM, capacity=5)
        self.conference_room = Room.objects.create(name="express24", type=RoomType.CONFERENCE, capacity=15)

    def test_room_detail(self):
        url = reverse("rooms-detail", kwargs={"pk": self.team_room.id})
        response = self.client.get(url)
        assert response.status_code == 200
        assert list(response.json().keys()) == ["id", "name", "type", "capacity"]
        assert response.json()["id"] == self.team_room.id
        assert response.json()["name"] == self.team_room.name
        assert response.json()["type"] == self.team_room.type
        assert response.json()["capacity"] == self.team_room.capacity

    def test_room_detail_invalid_pk(self):
        url = reverse("rooms-detail", kwargs={"pk": 111111111})
        response = self.client.get(url)
        assert response.status_code == 404
        assert response.json()["error"] == "topilmadi"
