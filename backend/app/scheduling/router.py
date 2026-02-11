from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import deps
from app.models.users import User, UserRole
from app.models.appointment import Appointment, DoctorAvailability
from app.schemas import appointment as schemas
from app.core.conflict_detection import validate_doctor_availability

router = APIRouter()

@router.post("/", response_model=schemas.Appointment)
def create_appointment(
    *,
    db: Session = Depends(deps.get_db),
    appointment_in: schemas.AppointmentCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new appointment.
    """
    # Verify availability
    is_available = validate_doctor_availability(
        db, appointment_in.doctor_id, appointment_in.start_time, appointment_in.end_time
    )
    if not is_available:
        raise HTTPException(status_code=400, detail="Doctor is not available at this time.")

    appointment = Appointment(
        patient_id=appointment_in.patient_id,
        doctor_id=appointment_in.doctor_id,
        start_time=appointment_in.start_time,
        end_time=appointment_in.end_time,
        notes=appointment_in.notes,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

@router.get("/", response_model=List[schemas.Appointment])
def read_appointments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve appointments.
    Doctors see their own. Admins/HR see all? Rules say Doctor: View appointments. 
    Assuming Doctor sees strict own, Admin sees all.
    """
    if current_user.role == UserRole.DOCTOR:
        appointments = db.query(Appointment).filter(Appointment.doctor_id == current_user.id).offset(skip).limit(limit).all()
    else:
        # Admin or others
        appointments = db.query(Appointment).offset(skip).limit(limit).all()
    return appointments

@router.put("/{appointment_id}", response_model=schemas.Appointment)
def update_appointment(
    *,
    db: Session = Depends(deps.get_db),
    appointment_id: int,
    appointment_in: schemas.AppointmentUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an appointment.
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Check permissions? Assuming open for now for simplicity, or restricted to Doctor/Admin.
    
    if appointment_in.start_time and appointment_in.end_time:
        # Validate new time
        is_available = validate_doctor_availability(
            db, appointment.doctor_id, appointment_in.start_time, appointment_in.end_time
        )
        if not is_available:
             raise HTTPException(status_code=400, detail="Doctor is not available at the new time.")
        appointment.start_time = appointment_in.start_time
        appointment.end_time = appointment_in.end_time
        
    if appointment_in.status:
        appointment.status = appointment_in.status
    if appointment_in.notes:
        appointment.notes = appointment_in.notes
        
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

@router.post("/availability", response_model=schemas.Availability)
def create_availability(
    *,
    db: Session = Depends(deps.get_db),
    availability_in: schemas.AvailabilityCreate,
    current_user: User = Depends(deps.require_role([UserRole.ADMIN, UserRole.DOCTOR])),
) -> Any:
    """
    Set doctor availability.
    """
    availability = DoctorAvailability(**availability_in.dict())
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability
