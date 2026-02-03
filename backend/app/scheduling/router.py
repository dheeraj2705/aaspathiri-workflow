"""Appointment scheduling API endpoints."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.auth.deps import get_current_active_user, require_role
from app.db.deps import get_db
from app.models import Appointment, User
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentRead,
    AppointmentUpdate,
)

router = APIRouter(prefix="/appointments", tags=["scheduling"])


@router.post(
    "",
    response_model=AppointmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment(
    appointment: AppointmentCreate,
    current_user: Annotated[User, Depends(require_role("admin"))],
    db: Annotated[Session, Depends(get_db)],
) -> AppointmentRead:
    """Create a new appointment.

    RBAC: Admin only.

    Validates:
    - Doctor exists
    - No double-booking (unique constraint on doctor_id, appointment_date, time_slot)

    Args:
        appointment: AppointmentCreate with patient_name, doctor_id, appointment_date, time_slot
        current_user: Authenticated admin user
        db: Database session

    Returns:
        AppointmentRead with created appointment data

    Raises:
        HTTPException: 400 if doctor not found or scheduling conflict exists
        HTTPException: 403 if user is not admin
    """
    # Verify doctor exists
    doctor = db.query(User).filter(User.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Doctor with id {appointment.doctor_id} not found",
        )

    # Check for scheduling conflict
    # Query: same doctor, same date, same time slot
    existing = db.query(Appointment).filter(
        and_(
            Appointment.doctor_id == appointment.doctor_id,
            Appointment.appointment_date == appointment.appointment_date,
            Appointment.time_slot == appointment.time_slot,
            Appointment.status != "cancelled",  # Allow rescheduled/cancelled slots
        )
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor already has an appointment in this time slot",
        )

    # Create appointment
    new_appointment = Appointment(
        patient_name=appointment.patient_name,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        time_slot=appointment.time_slot,
        status="scheduled",
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return AppointmentRead.model_validate(new_appointment)


@router.get("", response_model=list[AppointmentRead])
async def list_all_appointments(
    current_user: Annotated[User, Depends(require_role("admin"))],
    db: Annotated[Session, Depends(get_db)],
) -> list[AppointmentRead]:
    """List all appointments.

    RBAC: Admin only.

    Args:
        current_user: Authenticated admin user
        db: Database session

    Returns:
        List of all appointments

    Raises:
        HTTPException: 403 if user is not admin
    """
    appointments = db.query(Appointment).all()
    return [AppointmentRead.model_validate(a) for a in appointments]


@router.get("/me", response_model=list[AppointmentRead])
async def list_my_appointments(
    current_user: Annotated[User, Depends(require_role("doctor"))],
    db: Annotated[Session, Depends(get_db)],
) -> list[AppointmentRead]:
    """List appointments for the current doctor.

    RBAC: Doctor only (can only view their own appointments).

    Args:
        current_user: Authenticated doctor user
        db: Database session

    Returns:
        List of appointments for the current doctor

    Raises:
        HTTPException: 403 if user is not a doctor
    """
    appointments = db.query(Appointment).filter(
        Appointment.doctor_id == current_user.id
    ).all()
    return [AppointmentRead.model_validate(a) for a in appointments]
