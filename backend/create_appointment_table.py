#!/usr/bin/env python3
"""Create appointment table in PostgreSQL database."""

from app.db.base import Base
from app.db.session import engine
from app.models import Appointment

print("Creating 'appointments' table...")

# Create all tables (only creates if not exist)
Base.metadata.create_all(bind=engine)

print("✅ 'appointments' table created successfully!")
