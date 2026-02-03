"""Pydantic schemas for appointment scheduling."""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class AppointmentCreate(BaseModel):
    """Request schema for creating an appointment."""

    patient_name: str = Field(..., min_length=1, max_length=255)
    doctor_id: int = Field(..., gt=0)
    appointment_date: date
    time_slot: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Time slot format: HH:MM-HH:MM (e.g., 10:00-10:30)",
    )


class AppointmentUpdate(BaseModel):
    """Request schema for updating an appointment."""

    patient_name: str | None = Field(None, min_length=1, max_length=255)
    status: str | None = Field(None, min_length=1, max_length=50)


class AppointmentRead(BaseModel):
    """Response schema for appointment data."""

    id: int
    patient_name: str
    doctor_id: int
    appointment_date: date
    time_slot: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
