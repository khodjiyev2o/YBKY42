from datetime import datetime

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.rooms.models import Booking, Room, RoomType


class TestRoomBookView(APITestCase):
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

    def test_book_room_successfully(self):
        url = reverse("rooms-book", kwargs={"pk": 1})
        payload = {
            "resident": {"name": "Anvar Sanayev"},
            "start": "30-06-2023 09:00:00",
            "end": "30-06-2023 10:00:00",
        }
        response = self.client.post(url, data=payload, format='json')
        assert response.status_code == 201
        assert response.json()['message'] == 'xona muvaffaqiyatli band qilindi'


    def test_room_book_invalid_room_pk(self):
        url = reverse("rooms-book", kwargs={"pk": 11111111})
        data = {
            "resident": {"name": "Anvar Sanayev"},
            "start": "09-06-2023 09:00:00",
            "end": "09-06-2023 12:00:00",
        }
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 404
        assert response.json()["error"] == "Xona mavjud emas"


    def test_room_book_already_booked_time(self):
        url = reverse("rooms-book", kwargs={"pk": self.team_room.id})
        data = {
            "resident": {"name": "Anvar Sanayev"},
            "start": "09-06-2023 09:00:00",
            "end": "09-06-2023 12:00:00",
        }
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 410
        assert response.json()["error"] == "uzr, siz tanlagan vaqtda xona band"

    def test_room_book_start_time_after_end_time(self):
        url = reverse("rooms-book", kwargs={"pk": self.team_room.id})
        data = {
            "resident": {"name": "Anvar Sanayev"},
            "start": "09-06-2023 12:00:00",
            "end": "09-06-2023 9:00:00",
        }
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 404
        assert response.json()["error"] == "Notugri vaqt"

    def test_room_book_valid_date(self):
        url = reverse("rooms-book", kwargs={"pk": self.team_room.id})
        data = {
            "resident": {"name": "Anvar Sanayev"},
            "start": "09-07-2023 09:00:00",
            "end": "09-07-2023 12:00:00",
        }
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == 201
        assert response.json()["message"] == "xona muvaffaqiyatli band qilindi"
