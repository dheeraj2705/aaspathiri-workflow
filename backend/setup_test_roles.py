#!/usr/bin/env python3
"""Setup test data - Create default roles."""

from app.db.session import SessionLocal
from app.models import Role

db = SessionLocal()

roles_data = [
    {"name": "admin", "description": "Administrator with full access"},
    {"name": "hr", "description": "HR staff"},
    {"name": "doctor", "description": "Doctor"},
    {"name": "staff", "description": "Staff member"},
]

print("Setting up roles...")

for role_data in roles_data:
    existing = db.query(Role).filter(Role.name == role_data["name"]).first()
    if not existing:
        new_role = Role(**role_data)
        db.add(new_role)
        print(f"  Created role: {role_data['name']}")
    else:
        print(f"  Role already exists: {role_data['name']}")

db.commit()
print("\nRoles ready for testing!")
print("\nRole IDs:")
for role in db.query(Role).all():
    print(f"  {role.id}: {role.name}")

db.close()
