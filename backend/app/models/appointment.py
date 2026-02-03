"""SQLAlchemy model for appointment scheduling."""
from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Appointment(Base):
    """Appointment scheduling model.

    Non-clinical appointment tracking for hospital workflow.
    Prevents double-booking via unique constraint on (doctor_id, appointment_date, time_slot).
    """

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    # Non-clinical patient identifier (name only, no medical data)
    patient_name = Column(String(255), nullable=False, index=True)

    # Foreign key to doctor (user with doctor role)
    doctor_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Appointment date (no clinical info in time)
    appointment_date = Column(Date, nullable=False, index=True)

    # Time slot as string (e.g., "10:00-10:30", "14:00-14:30")
    time_slot = Column(String(50), nullable=False)

    # Appointment status: "scheduled", "completed", "cancelled"
    status = Column(String(50), default="scheduled", nullable=False, index=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationship to doctor (User model)
    doctor = relationship("User", foreign_keys=[doctor_id])

    # Unique constraint: one appointment per doctor per time slot per day
    __table_args__ = (
        UniqueConstraint(
            "doctor_id",
            "appointment_date",
            "time_slot",
            name="uq_doctor_date_timeslot",
        ),
    )

    def __repr__(self) -> str:
        """String representation of appointment."""
        return (
            f"<Appointment(id={self.id}, doctor_id={self.doctor_id}, "
            f"date={self.appointment_date}, slot={self.time_slot}, "
            f"status={self.status})>"
        )
