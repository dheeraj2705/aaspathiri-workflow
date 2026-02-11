from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Date, Time
from sqlalchemy.orm import relationship
from app.core.db import Base
import enum

class RoomType(str, enum.Enum):
    CONSULTATION = "consultation"
    WARD = "ward"
    ICU = "icu"
    OT = "ot"

class RoomStatus(str, enum.Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(Enum(RoomType), nullable=False)
    status = Column(Enum(RoomStatus), default=RoomStatus.AVAILABLE)
    capacity = Column(Integer, default=1)

class OTSlotStatus(str, enum.Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    MAINTENANCE = "maintenance"

class OTSlot(Base):
    __tablename__ = "ot_slots"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum(OTSlotStatus), default=OTSlotStatus.AVAILABLE)

    room = relationship("Room", backref="ot_slots")

class OTBooking(Base):
    __tablename__ = "ot_bookings"

    id = Column(Integer, primary_key=True, index=True)
    ot_slot_id = Column(Integer, ForeignKey("ot_slots.id"), nullable=False)
    patient_id = Column(Integer, nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    procedure_name = Column(String, nullable=False)
    status = Column(String, default="confirmed") # confirmed, cancelled

    slot = relationship("OTSlot", backref="bookings")
    doctor = relationship("User", backref="ot_bookings")
