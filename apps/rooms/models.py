from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel

from .choices import RoomType
from .managers import RoomManager


class Room(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    type = models.CharField(max_length=63, verbose_name=_("Room Type"), choices=RoomType.choices)
    capacity = models.PositiveIntegerField(verbose_name=_("Capacity"))
    objects = RoomManager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        ordering = ["id"]


class Booking(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    start_time = models.DateTimeField(verbose_name=_("Start Time"))
    end_time = models.DateTimeField(verbose_name=_("End Time"))

    def __str__(self):
        return f"Room: {self.room} | {self.start_time} to {self.end_time}"

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
