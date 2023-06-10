from datetime import datetime

from django.utils import timezone


def get_availability(self, date=None):
    if not date:
        date = timezone.localdate()
    else:
        date = datetime.strptime(date, "%d-%m-%Y").date()

    start_time = timezone.make_aware(timezone.datetime(date.year, date.month, date.day, 9, 0, 0))
    end_time = timezone.make_aware(timezone.datetime(date.year, date.month, date.day, 18, 0, 0))

    booked_slots = self.bookings.filter(start_time__date=date, end_time__date=date).order_by("start_time")
    availability = []

    if not booked_slots.exists():
        availability.append(
            {
                "start": timezone.localtime(start_time).strftime("%d-%m-%Y %H:%M:%S"),
                "end": timezone.localtime(end_time).strftime("%d-%m-%Y %H:%M:%S"),
            }
        )
    else:
        current_slot_start = start_time.replace(hour=9)
        for booked_slot in booked_slots:
            if current_slot_start < booked_slot.start_time:
                availability.append(
                    {
                        "start": timezone.localtime(current_slot_start).strftime("%d-%m-%Y %H:%M:%S"),
                        "end": timezone.localtime(booked_slot.start_time).strftime("%d-%m-%Y %H:%M:%S"),
                    }
                )
            current_slot_start = booked_slot.end_time

        if current_slot_start < end_time.replace(hour=18, minute=0, second=0):
            availability.append(
                {
                    "start": timezone.localtime(current_slot_start).strftime("%d-%m-%Y %H:%M:%S"),
                    "end": timezone.localtime(end_time.replace(hour=18, minute=0, second=0)).strftime(
                        "%d-%m-%Y %H:%M:%S"
                    ),
                }
            )

    """ if the whole day is booked """
    if availability == [
        {
            "start": timezone.localtime(end_time.replace(hour=18, minute=0, second=0)).strftime("%d-%m-%Y %H:%M:%S"),
            "end": timezone.localtime(end_time.replace(hour=18, minute=0, second=0)).strftime("%d-%m-%Y %H:%M:%S"),
        }
    ]:
        return {"error": "uzr, siz tanlagan vaqtda xona band"}

    return availability
