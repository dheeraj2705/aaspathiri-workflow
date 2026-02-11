from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.appointment import Appointment, AppointmentStatus, DoctorAvailability
from app.models.room import OTSlot, OTBooking, OTSlotStatus
from app.models.shift import Shift, StaffShiftAssignment, ShiftAssignmentStatus

def check_time_overlap(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool:
    """
    Returns True if the time ranges overlap.
    """
    return max(start1, start2) < min(end1, end2)

def validate_doctor_availability(db: Session, doctor_id: int, start_time: datetime, end_time: datetime) -> bool:
    """
    Validates if a doctor is available:
    1. Checks if the time slot is within their working hours (DoctorAvailability).
    2. Checks if they have any overlapping appointments.
    Returns True if available, False otherwise.
    """
    # 1. Check working hours (simplified: assumes weekly schedule)
    day_of_week = start_time.weekday() # 0=Monday
    availability = db.query(DoctorAvailability).filter(
        DoctorAvailability.doctor_id == doctor_id,
        DoctorAvailability.day_of_week == day_of_week
    ).first()

    if not availability:
        # If no availability defined, assume unavailable or default? 
        # Requirement says "Availability validation before booking". 
        # If not defined, let's assume valid for now OR invalid. Safe bet: Invalid if not explicitly available.
        return False
    
    # Check time boundaries
    # Convert datetime to time for comparison
    req_start = start_time.time()
    req_end = end_time.time()
    
    if req_start < availability.start_time or req_end > availability.end_time:
        return False

    # 2. Check existing appointments
    overlap = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.status == AppointmentStatus.SCHEDULED,
        or_(
            and_(Appointment.start_time < end_time, Appointment.start_time >= start_time),
            and_(Appointment.end_time > start_time, Appointment.end_time <= end_time),
            and_(Appointment.start_time <= start_time, Appointment.end_time >= end_time)
        )
    ).first()

    if overlap:
        return False

    return True

def validate_ot_availability(db: Session, ot_slot_id: int) -> bool:
    """
    Checks if an OT slot is available for booking.
    """
    slot = db.query(OTSlot).filter(OTSlot.id == ot_slot_id).first()
    if not slot or slot.status != OTSlotStatus.AVAILABLE:
        return False
    
    # Check if already booked (redundant if status is managed well, but safer)
    booking = db.query(OTBooking).filter(OTBooking.ot_slot_id == ot_slot_id, OTBooking.status != "cancelled").first()
    if booking:
        return False
        
    return True

def validate_shift_overlap(db: Session, staff_id: int, start_time: datetime, end_time: datetime) -> bool:
    """
    Checks if a staff member already has an overlapping shift.
    """
    # Find all shifts assigned to this staff
    assignments = db.query(StaffShiftAssignment).filter(
        StaffShiftAssignment.staff_id == staff_id,
        StaffShiftAssignment.status.in_([ShiftAssignmentStatus.ASSIGNED, ShiftAssignmentStatus.SWAPPED])
    ).all()
    
    for assignment in assignments:
        shift = assignment.shift
        # Check overlap
        if check_time_overlap(start_time, end_time, shift.start_time, shift.end_time):
            return False
            
    return True
