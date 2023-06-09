from django.urls import reverse
from rest_framework.test import APITestCase

from apps.rooms.models import Room, RoomType


class TestRoomView(APITestCase):
    url = reverse("rooms-list")

    def setUp(self):
        self.team_room = Room.objects.create(name="workly", type=RoomType.TEAM, capacity=5)
        self.conference_room = Room.objects.create(name="express24", type=RoomType.CONFERENCE, capacity=15)

    def test_room_list(self):
        response = self.client.get(self.url)
        assert response.json()["page"] == 1
        assert response.json()["count"] == 2
        assert response.json()["page_size"] == 10
        assert response.status_code == 200
        assert list(response.json().keys()) == ["page", "count", "page_size", "results"]
        assert list(response.json()["results"][0].keys()) == ["id", "name", "type", "capacity"]

    def test_room_list_filter_by_type(self):
        response = self.client.get(f"{self.url}?type={RoomType.TEAM}")
        assert response.json()["page"] == 1
        assert response.json()["count"] == 1
        assert response.json()["page_size"] == 10
        assert response.status_code == 200
        assert list(response.json().keys()) == ["page", "count", "page_size", "results"]
        assert list(response.json()["results"][0].keys()) == ["id", "name", "type", "capacity"]
        assert response.json()["results"][0]["id"] == self.team_room.id
        assert response.json()["results"][0]["name"] == self.team_room.name
        assert response.json()["results"][0]["type"] == self.team_room.type
        assert response.json()["results"][0]["capacity"] == self.team_room.capacity

    def test_room_list_search_by_name(self):
        response = self.client.get(f"{self.url}?search={self.conference_room.name}")
        assert response.json()["page"] == 1
        assert response.json()["count"] == 1
        assert response.json()["page_size"] == 10
        assert response.status_code == 200
        assert list(response.json().keys()) == ["page", "count", "page_size", "results"]
        assert list(response.json()["results"][0].keys()) == ["id", "name", "type", "capacity"]
        assert response.json()["results"][0]["id"] == self.conference_room.id
        assert response.json()["results"][0]["name"] == self.conference_room.name
        assert response.json()["results"][0]["type"] == self.conference_room.type
        assert response.json()["results"][0]["capacity"] == self.conference_room.capacity

    def test_room_list_search_by_name_invalid_data(self):
        response = self.client.get(f"{self.url}?search=something_Wrong")
        assert response.json()["page"] == 1
        assert response.json()["count"] == 0
        assert response.json()["page_size"] == 10
        assert response.status_code == 200
        assert list(response.json().keys()) == ["page", "count", "page_size", "results"]
        assert response.json()["results"] == []

    def test_room_list_filter_by_type_no_type_data(self):
        response = self.client.get(f"{self.url}?type={RoomType.FOCUS}")
        assert response.json()["page"] == 1
        assert response.json()["count"] == 0
        assert response.json()["page_size"] == 10
        assert response.status_code == 200
        assert list(response.json().keys()) == ["page", "count", "page_size", "results"]
        assert response.json()["results"] == []
