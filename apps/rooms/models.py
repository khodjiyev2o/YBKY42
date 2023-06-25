from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel

from .choices import RoomType
from .exceptions import InvalidTimeError
from .utils import get_availability
from datetime import datetime


class Room(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"), unique=True)
    type = models.CharField(max_length=63, verbose_name=_("Room Type"), choices=RoomType.choices)
    capacity = models.PositiveIntegerField(verbose_name=_("Capacity"))

    def __str__(self):
        return f"{self.name}"

    def availability(self, date=None) -> dict:
        return get_availability(self=self, date=date)

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        ordering = ["id"]


class Booking(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    resident = models.CharField(max_length=255, verbose_name=_("Resident"))
    start = models.DateTimeField(verbose_name=_("Start Time"))
    end = models.DateTimeField(verbose_name=_("End Time"))

    def __str__(self):
        return f"Room: {self.room} | {self.start} to {self.end}"

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Booking")

    def clean(self):
        """Check if there are any bookings in the given timeline before creating new one"""

        if self.start and self.end:
            conflicting_bookings = Booking.objects.filter(
                room=self.room, start__lt=self.end, end__gt=self.start
            )
            if conflicting_bookings.exists():
                raise ValidationError(_("uzr, siz tanlagan vaqtda xona band"))

        """Start time should not be greater, than end_time"""
        if self.start >= self.end:
            raise InvalidTimeError(_("Notugri, vaqt"))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
