from datetime import datetime

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.rooms.models import Booking, Room, RoomType


class TestRoomAvailabilityView(APITestCase):
    date = timezone.localdate()

    start_time = timezone.make_aware(timezone.datetime(date.year, date.month, date.day, 9, 0, 0))
    end_time = timezone.make_aware(timezone.datetime(date.year, date.month, date.day, 18, 0, 0))

    def setUp(self):
        self.team_room = Room.objects.create(name="workly", type=RoomType.TEAM, capacity=5)
        self.conference_room = Room.objects.create(name="express24", type=RoomType.CONFERENCE, capacity=15)
        self.booking_team_room = Booking.objects.create(
            start=timezone.make_aware(datetime(2023, 6, 9, 9, 0, 0)),
            end=timezone.make_aware(datetime(2023, 6, 9, 12, 0, 0)),
            room=self.team_room,
            resident="Samandar",
        )
        self.booking_conference_room = Booking.objects.create(
            start=timezone.make_aware(datetime(2023, 6, 9, 11, 0, 0)),
            end=timezone.make_aware(datetime(2023, 6, 9, 12, 0, 0)),
            room=self.conference_room,
            resident="Samandar",
        )

    def test_room_availability_today_without_date(self):
        url = reverse("rooms-availability", kwargs={"pk": self.team_room.id})
        response = self.client.get(url)
        assert response.status_code == 200
        assert list(response.json()[0].keys()) == ["start", "end"]
        assert response.json()[0]["start"] == timezone.localtime(self.start_time).strftime("%d-%m-%Y %H:%M:%S")
        assert response.json()[0]["end"] == timezone.localtime(self.end_time).strftime("%d-%m-%Y %H:%M:%S")

    def test_room_availability_today_with_date_params(self):
        day, month, year = self.date.day, self.date.month, self.date.year
        url = reverse("rooms-availability", kwargs={"pk": self.team_room.id})
        response = self.client.get(f"{url}?date={day}-{month}-{year}")
        assert response.status_code == 200
        assert list(response.json()[0].keys()) == ["start", "end"]
        assert response.json()[0]["start"] == timezone.localtime(self.start_time).strftime("%d-%m-%Y %H:%M:%S")
        assert response.json()[0]["end"] == timezone.localtime(self.end_time).strftime("%d-%m-%Y %H:%M:%S")

    def test_room_availability_with_booked_time_valid_time(self):
        url = reverse("rooms-availability", kwargs={"pk": self.team_room.id})
        response = self.client.get(f"{url}?date=09-06-2023")
        assert response.status_code == 200
        assert list(response.json()[0].keys()) == ["start", "end"]
        assert response.json()[0]["start"] == "09-06-2023 12:00:00"
        assert response.json()[0]["end"] == "09-06-2023 18:00:00"

    def test_room_availability_with_booked_time_2_valid_time(self):
        url = reverse("rooms-availability", kwargs={"pk": self.conference_room.id})
        response = self.client.get(f"{url}?date=09-06-2023")
        assert response.status_code == 200
        assert list(response.json()[0].keys()) == ["start", "end"]
        assert response.json()[0]["start"] == "09-06-2023 09:00:00"
        assert response.json()[0]["end"] == "09-06-2023 11:00:00"
        assert response.json()[1]["start"] == "09-06-2023 12:00:00"
        assert response.json()[1]["end"] == "09-06-2023 18:00:00"

    def test_room_availability_non_existing_room(self):
        url = reverse("rooms-availability", kwargs={"pk": 11111111})
        response = self.client.get(f"{url}?date=09-06-2023")
        assert response.status_code == 404
        assert response.json()["error"] == "Xona mavjud emas"
