from pydantic import BaseModel, Field
from datetime import date


class AvailabilityResponse(BaseModel):
    date: str
    appointment_type: str
    available_slots: list[str]


class AvailabilityRequest(BaseModel):
    date: str
    appointment_type: str


class BookingRequest(BaseModel):
    patient_name: str
    appointment_type: str
    date: date
    start_time: str


class BookingResponse(BaseModel):
    id: int
    patient_name: str
    appointment_type: str
    date: date
    start_time: str
    duration: int
