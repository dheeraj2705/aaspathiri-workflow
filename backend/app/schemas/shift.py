from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.shift import ShiftType, ShiftAssignmentStatus

class ShiftBase(BaseModel):
    name: Optional[str] = None
    start_time: datetime
    end_time: datetime
    type: ShiftType

class ShiftCreate(ShiftBase):
    pass

class Shift(ShiftBase):
    id: int

    class Config:
        from_attributes = True

class ShiftAssignmentBase(BaseModel):
    staff_id: int
    shift_id: int
    status: ShiftAssignmentStatus = ShiftAssignmentStatus.ASSIGNED

class ShiftAssignmentCreate(ShiftAssignmentBase):
    pass

class ShiftAssignment(ShiftAssignmentBase):
    id: int

    class Config:
        from_attributes = True

class ShiftSwapRequest(BaseModel):
    assignment_id: int
    target_staff_id: int
