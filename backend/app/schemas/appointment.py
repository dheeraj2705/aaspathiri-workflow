from typing import Optional, List
from datetime import datetime, time, date
from pydantic import BaseModel
from app.models.appointment import AppointmentStatus

class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None

class AppointmentInDBBase(AppointmentBase):
    id: int
    status: AppointmentStatus

    class Config:
        from_attributes = True

class Appointment(AppointmentInDBBase):
    pass

class AvailabilityBase(BaseModel):
    doctor_id: int
    day_of_week: int
    start_time: time
    end_time: time

class AvailabilityCreate(AvailabilityBase):
    pass

class Availability(AvailabilityBase):
    id: int

    class Config:
        from_attributes = True
