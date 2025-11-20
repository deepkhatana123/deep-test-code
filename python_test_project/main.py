from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta, time
from schema import AvailabilityRequest, BookingRequest, BookingResponse, AvailabilityResponse
from database import appointment_types, bookings
from utils import generate_daily_slots, detect_available_slots

app = FastAPI(title="Mock Calendly API", version="1.0")


@app.get("/api/calendly/availability", response_model=AvailabilityResponse)
async def get_availability(date: str, appointment_type: str):
    # Validate appointment type
    if appointment_type not in appointment_types:
        raise HTTPException(status_code=400, detail="Invalid appointment type")

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    duration = appointment_types[appointment_type]["duration"]

    # Generate raw clinic slots
    all_slots = generate_daily_slots(
        date=date_obj,
        start=time(9, 0),
        end=time(17, 0),
        duration_minutes=duration
    )

    # Remove booked slots
    available_slots = detect_available_slots(date_obj, all_slots, duration)

    return AvailabilityResponse(
        date=str(date_obj),
        appointment_type=appointment_type,
        available_slots=available_slots
    )


@app.post("/api/calendly/book", response_model=BookingResponse)
async def book_appointment(payload: BookingRequest):
    # Validate appointment type
    if payload.appointment_type not in appointment_types:
        raise HTTPException(status_code=400, detail="Invalid appointment type")

    date_obj = payload.date
    duration = appointment_types[payload.appointment_type]["duration"]

    # Generate full day's raw slots
    all_slots = generate_daily_slots(
        date=date_obj,
        start=time(9, 0),
        end=time(17, 0),
        duration_minutes=duration
    )

    # Check if requested slot is valid
    if payload.start_time not in all_slots:
        raise HTTPException(status_code=400, detail="Invalid time slot")

    # Check if already booked
    for b in bookings:
        if b["date"] == payload.date and b["start_time"] == payload.start_time:
            raise HTTPException(status_code=400, detail="Slot already booked")

    # Save booking (mock database)
    booking = {
        "id": len(bookings) + 1,
        "patient_name": payload.patient_name,
        "appointment_type": payload.appointment_type,
        "date": payload.date,
        "start_time": payload.start_time,
        "duration": duration,
    }
    bookings.append(booking)

    return BookingResponse(**booking)
