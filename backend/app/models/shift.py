from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Date, Time
from sqlalchemy.orm import relationship
from app.core.db import Base
import enum

class ShiftType(str, enum.Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    NIGHT = "night"

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True) # e.g., "Morning Shift A"
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    type = Column(Enum(ShiftType), nullable=False)

class ShiftAssignmentStatus(str, enum.Enum):
    ASSIGNED = "assigned"
    COMPLETED = "completed"
    SWAP_REQUESTED = "swap_requested"
    SWAPPED = "swapped"

class StaffShiftAssignment(Base):
    __tablename__ = "staff_shift_assignments"

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    status = Column(Enum(ShiftAssignmentStatus), default=ShiftAssignmentStatus.ASSIGNED)

    staff = relationship("User", backref="shift_assignments")
    shift = relationship("Shift", backref="assignments")
