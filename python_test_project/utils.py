from datetime import datetime, timedelta


def generate_daily_slots(date, start, end, duration_minutes):
    ##Generate time slots for entire day.
    slots = []
    current = datetime.combine(date, start)
    end_dt = datetime.combine(date, end)

    while current + timedelta(minutes=duration_minutes) <= end_dt:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=duration_minutes)

    return slots


def detect_available_slots(date, all_slots, duration):
    from app.database import bookings

    booked = {
        b["start_time"]
        for b in bookings
        if b["date"] == date
    }

    return [slot for slot in all_slots if slot not in booked]
