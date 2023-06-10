from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel

from .choices import RoomType
from .managers import get_availability


class Room(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
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
    start_time = models.DateTimeField(verbose_name=_("Start Time"))
    end_time = models.DateTimeField(verbose_name=_("End Time"))

    def __str__(self):
        return f"Room: {self.room} | {self.start_time} to {self.end_time}"

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Booking")

    def clean(self):
        if self.start_time and self.end_time:
            conflicting_bookings = Booking.objects.filter(
                room=self.room, start_time__lt=self.end_time, end_time__gt=self.start_time
            )
            if conflicting_bookings.exists():
                raise ValidationError(_("Booking conflicts with an existing booking."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
