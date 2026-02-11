from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.room import RoomType, RoomStatus, OTSlotStatus

class RoomBase(BaseModel):
    name: str
    type: RoomType
    status: RoomStatus = RoomStatus.AVAILABLE
    capacity: int = 1

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int

    class Config:
        from_attributes = True

class OTSlotBase(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime
    status: OTSlotStatus = OTSlotStatus.AVAILABLE

class OTSlotCreate(OTSlotBase):
    pass

class OTSlot(OTSlotBase):
    id: int

    class Config:
        from_attributes = True

class OTBookingBase(BaseModel):
    ot_slot_id: int
    patient_id: int
    doctor_id: int
    procedure_name: str

class OTBookingCreate(OTBookingBase):
    pass

class OTBooking(OTBookingBase):
    id: int
    status: str

    class Config:
        from_attributes = True
