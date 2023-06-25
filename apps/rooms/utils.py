from datetime import datetime

from django.utils import timezone


def get_availability(self, date=None):
    if not date:
        date = timezone.localdate()
    else:
        date = datetime.strptime(date, "%d-%m-%Y").date()

    start_time = timezone.make_aware(timezone.datetime.combine(date, datetime.min.time()))
    end_time = timezone.make_aware(timezone.datetime.combine(date, datetime.max.time()))

    booked_slots = self.bookings.filter(start__date=date, end__date=date).order_by("start")
    availability = []

    if not booked_slots.exists():
        availability.append(
            {
                "start": timezone.localtime(start_time).strftime("%d-%m-%Y %H:%M:%S"),
                "end": timezone.localtime(end_time).strftime("%d-%m-%Y %H:%M:%S"),
            }
        )
    else:
        current_slot_start = start_time
        for booked_slot in booked_slots:
            if current_slot_start < booked_slot.start:
                availability.append(
                    {
                        "start": timezone.localtime(current_slot_start).strftime("%d-%m-%Y %H:%M:%S"),
                        "end": timezone.localtime(booked_slot.start).strftime("%d-%m-%Y %H:%M:%S"),
                    }
                )
            current_slot_start = booked_slot.end

        if current_slot_start < end_time:
            availability.append(
                {
                    "start": timezone.localtime(current_slot_start).strftime("%d-%m-%Y %H:%M:%S"),
                    "end": timezone.localtime(end_time).strftime("%d-%m-%Y %H:%M:%S"),
                }
            )

    # Remove the availability slot if it covers the entire day.
    availability = [slot for slot in availability if slot["start"] != slot["end"]]

    return availability

