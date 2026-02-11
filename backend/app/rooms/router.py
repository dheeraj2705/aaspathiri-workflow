from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import deps
from app.models.users import User, UserRole
from app.models.room import Room, OTSlot, OTBooking, OTSlotStatus
from app.schemas import room as schemas
from app.core.conflict_detection import validate_ot_availability

router = APIRouter()

@router.post("/", response_model=schemas.Room)
def create_room(
    *,
    db: Session = Depends(deps.get_db),
    room_in: schemas.RoomCreate,
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
) -> Any:
    """
    Create a new room (Admin only).
    """
    room = Room(**room_in.dict())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@router.get("/", response_model=List[schemas.Room])
def read_rooms(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    List all rooms.
    """
    rooms = db.query(Room).offset(skip).limit(limit).all()
    return rooms

@router.post("/ot-slots", response_model=schemas.OTSlot)
def create_ot_slot(
    *,
    db: Session = Depends(deps.get_db),
    slot_in: schemas.OTSlotCreate,
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
) -> Any:
    """
    Create an OT slot (Admin only).
    """
    slot = OTSlot(**slot_in.dict())
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot

@router.post("/ot-bookings", response_model=schemas.OTBooking)
def book_ot_slot(
    *,
    db: Session = Depends(deps.get_db),
    booking_in: schemas.OTBookingCreate,
    current_user: User = Depends(deps.require_role([UserRole.DOCTOR, UserRole.ADMIN])),
) -> Any:
    """
    Book an OT slot.
    """
    # Check availability
    is_available = validate_ot_availability(db, booking_in.ot_slot_id)
    if not is_available:
        raise HTTPException(status_code=400, detail="OT Slot is not available")
    
    booking = OTBooking(**booking_in.dict())
    
    # Update slot status to booked? 
    # Logic: if slot is booked, it's unavailable.
    slot = db.query(OTSlot).get(booking_in.ot_slot_id)
    slot.status = OTSlotStatus.BOOKED
    
    db.add(booking)
    db.add(slot)
    db.commit()
    db.refresh(booking)
    return booking
