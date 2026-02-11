from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import deps
from app.models.users import User, UserRole
from app.models.shift import Shift, StaffShiftAssignment, ShiftAssignmentStatus
from app.schemas import shift as schemas
from app.core.conflict_detection import validate_shift_overlap

router = APIRouter()

@router.post("/", response_model=schemas.Shift)
def create_shift(
    *,
    db: Session = Depends(deps.get_db),
    shift_in: schemas.ShiftCreate,
    current_user: User = Depends(deps.require_role([UserRole.ADMIN, UserRole.HR])),
) -> Any:
    """
    Create a new shift (HR/Admin only).
    """
    shift = Shift(**shift_in.dict())
    db.add(shift)
    db.commit()
    db.refresh(shift)
    return shift

@router.post("/assign", response_model=schemas.ShiftAssignment)
def assign_shift(
    *,
    db: Session = Depends(deps.get_db),
    assignment_in: schemas.ShiftAssignmentCreate,
    current_user: User = Depends(deps.require_role([UserRole.ADMIN, UserRole.HR])),
) -> Any:
    """
    Assign staff to a shift.
    """
    # Check overlap
    shift = db.query(Shift).get(assignment_in.shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    is_valid = validate_shift_overlap(db, assignment_in.staff_id, shift.start_time, shift.end_time)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Staff has overlapping shift.")

    assignment = StaffShiftAssignment(**assignment_in.dict())
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.get("/my-shifts", response_model=List[schemas.ShiftAssignment])
def read_my_shifts(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    View personal shifts.
    """
    assignments = db.query(StaffShiftAssignment).filter(StaffShiftAssignment.staff_id == current_user.id).all()
    return assignments

@router.post("/swap", response_model=schemas.ShiftAssignment)
def request_swap(
     *,
    db: Session = Depends(deps.get_db),
    swap_request: schemas.ShiftSwapRequest,
    current_user: User = Depends(deps.require_role([UserRole.STAFF, UserRole.DOCTOR])), # Anyone can request?
) -> Any:
    """
    Request shift swap.
    """
    assignment = db.query(StaffShiftAssignment).get(swap_request.assignment_id)
    if not assignment:
         raise HTTPException(status_code=404, detail="Assignment not found")
    
    if assignment.staff_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your shift")
        
    assignment.status = ShiftAssignmentStatus.SWAP_REQUESTED
    # In a real app, we'd store the target_staff_id somewhere to approve it later. 
    # For now, simplistic implementation just marking query.
    
    db.commit()
    db.refresh(assignment)
    return assignment

@router.post("/swap/approve/{assignment_id}", response_model=schemas.ShiftAssignment)
def approve_swap(
    *,
    db: Session = Depends(deps.get_db),
    assignment_id: int,
    current_user: User = Depends(deps.require_role([UserRole.HR, UserRole.ADMIN])),
) -> Any:
    """
    Approve shift swap (HR/Admin).
    """
    assignment = db.query(StaffShiftAssignment).get(assignment_id)
    if not assignment:
         raise HTTPException(status_code=404, detail="Assignment not found")
         
    if assignment.status != ShiftAssignmentStatus.SWAP_REQUESTED:
        raise HTTPException(status_code=400, detail="Swap not requested")

    assignment.status = ShiftAssignmentStatus.SWAPPED
    db.commit()
    db.refresh(assignment)
    return assignment
