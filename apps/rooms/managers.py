from django.db import models
from django.utils import timezone


class RoomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("bookings")

    def get_availability(self, date=None):
        if not date:
            date = timezone.localdate()

        start_time = timezone.datetime.combine(date, timezone.datetime.min.time())
        end_time = timezone.datetime.combine(date, timezone.datetime.max.time())

        booked_slots = self.bookings.filter(start_time__date=date, end_time__date=date).order_by("start_time")

        availability = []

        if not booked_slots.exists():
            availability.append(
                {
                    "start": start_time.replace(hour=9).strftime("%d-%m-%Y %H:%M:%S"),
                    "end": end_time.replace(hour=18).strftime("%d-%m-%Y %H:%M:%S"),
                }
            )
        else:
            current_slot_start = start_time.replace(hour=9)
            for booked_slot in booked_slots:
                if current_slot_start < booked_slot.start_time:
                    availability.append(
                        {
                            "start": current_slot_start.strftime("%d-%m-%Y %H:%M:%S"),
                            "end": booked_slot.start_time.strftime("%d-%m-%Y %H:%M:%S"),
                        }
                    )
                current_slot_start = booked_slot.end_time

            if current_slot_start < end_time.replace(hour=18):
                availability.append(
                    {
                        "start": current_slot_start.strftime("%d-%m-%Y %H:%M:%S"),
                        "end": end_time.replace(hour=18).strftime("%d-%m-%Y %H:%M:%S"),
                    }
                )

        return availability
