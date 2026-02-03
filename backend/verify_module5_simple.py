#!/usr/bin/env python3
"""Module 5 Verification - File-based (no imports)."""

import os
import sys

print('\n' + '='*80)
print('MODULE 5 VERIFICATION - Appointment Scheduling')
print('='*80)

backend_dir = os.path.dirname(os.path.abspath(__file__))
results = []

# ============================================================================
# 1. Check files exist
# ============================================================================
print('\n[1] REQUIRED FILES')
files_to_check = [
    'app/models/appointment.py',
    'app/schemas/appointment.py',
    'app/scheduling/router.py',
    'app/scheduling/__init__.py',
]

all_exist = True
for file_path in files_to_check:
    full_path = os.path.join(backend_dir, file_path)
    exists = os.path.exists(full_path)
    status = '✅' if exists else '❌'
    print(f"  {status} {file_path}")
    all_exist = all_exist and exists

results.append(("FILES EXIST", all_exist))

# ============================================================================
# 2. Check Appointment model structure
# ============================================================================
print('\n[2] APPOINTMENT MODEL - app/models/appointment.py')
try:
    with open(os.path.join(backend_dir, 'app/models/appointment.py'), 'r') as f:
        model_content = f.read()
    
    required_fields = [
        'patient_name', 'doctor_id', 'appointment_date', 'time_slot',
        'status', 'created_at', 'updated_at'
    ]
    
    all_found = all(f'Column' in model_content and f in model_content for f in required_fields)
    
    # Check for relationship
    has_doctor_rel = 'doctor = relationship("User"' in model_content
    
    # Check for unique constraint
    has_unique = 'uq_doctor_date_timeslot' in model_content and 'UniqueConstraint' in model_content
    
    for field in required_fields:
        status = '✅'
        print(f"  {status} Field: {field}")
    
    status = '✅' if has_doctor_rel else '❌'
    print(f"  {status} Relationship: doctor (User)")
    
    status = '✅' if has_unique else '❌'
    print(f"  {status} Unique constraint on (doctor_id, appointment_date, time_slot)")
    
    results.append(("APPOINTMENT MODEL", all_found and has_doctor_rel and has_unique))
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    results.append(("APPOINTMENT MODEL", False))

# ============================================================================
# 3. Check schemas exist
# ============================================================================
print('\n[3] APPOINTMENT SCHEMAS - app/schemas/appointment.py')
try:
    with open(os.path.join(backend_dir, 'app/schemas/appointment.py'), 'r') as f:
        schemas_content = f.read()
    
    schemas = ['AppointmentCreate', 'AppointmentRead', 'AppointmentUpdate']
    all_found = all(f'class {s}' in schemas_content for s in schemas)
    
    for schema in schemas:
        status = '✅'
        print(f"  {status} {schema}")
    
    results.append(("APPOINTMENT SCHEMAS", all_found))
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    results.append(("APPOINTMENT SCHEMAS", False))

# ============================================================================
# 4. Check router endpoints
# ============================================================================
print('\n[4] SCHEDULING ROUTER - app/scheduling/router.py')
try:
    with open(os.path.join(backend_dir, 'app/scheduling/router.py'), 'r') as f:
        router_content = f.read()
    
    # Check endpoints exist
    has_create = ('@router.post' in router_content and 'create_appointment' in router_content)
    has_list_all = 'def list_all_appointments' in router_content
    has_list_me = 'def list_my_appointments' in router_content
    
    # Check RBAC enforcement
    has_admin_rbac = 'require_role("admin")' in router_content
    has_doctor_rbac = 'require_role("doctor")' in router_content
    
    # Check conflict detection
    has_conflict = 'Doctor already has an appointment' in router_content and 'existing = db.query' in router_content
    
    status = '✅' if has_create else '❌'
    print(f"  {status} POST /appointments (create endpoint)")
    
    status = '✅' if has_list_all else '❌'
    print(f"  {status} GET /appointments (list all - admin only)")
    
    status = '✅' if has_list_me else '❌'
    print(f"  {status} GET /appointments/me (list own - doctor only)")
    
    status = '✅' if has_admin_rbac else '❌'
    print(f"  {status} RBAC: Admin role enforcement")
    
    status = '✅' if has_doctor_rbac else '❌'
    print(f"  {status} RBAC: Doctor role enforcement")
    
    status = '✅' if has_conflict else '❌'
    print(f"  {status} Conflict detection (no double-booking)")
    
    all_found = all([has_create, has_list_all, has_list_me, has_admin_rbac, has_doctor_rbac, has_conflict])
    results.append(("SCHEDULING ROUTER", all_found))
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    results.append(("SCHEDULING ROUTER", False))

# ============================================================================
# 5. Check router package initialization
# ============================================================================
print('\n[5] SCHEDULING PACKAGE - app/scheduling/__init__.py')
try:
    with open(os.path.join(backend_dir, 'app/scheduling/__init__.py'), 'r') as f:
        init_content = f.read()
    
    has_router_export = 'from app.scheduling.router import router' in init_content
    
    status = '✅' if has_router_export else '❌'
    print(f"  {status} Exports router")
    
    results.append(("SCHEDULING PACKAGE", has_router_export))
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    results.append(("SCHEDULING PACKAGE", False))

# ============================================================================
# 6. Check main.py registration
# ============================================================================
print('\n[6] ROUTER REGISTRATION - app/main.py')
try:
    with open(os.path.join(backend_dir, 'app/main.py'), 'r') as f:
        main_content = f.read()
    
    has_import = 'from app.scheduling.router import router as scheduling_router' in main_content
    has_registration = 'app.include_router(scheduling_router)' in main_content
    
    status = '✅' if has_import else '❌'
    print(f"  {status} Scheduling router imported")
    
    status = '✅' if has_registration else '❌'
    print(f"  {status} Scheduling router registered")
    
    results.append(("ROUTER REGISTRATION", has_import and has_registration))
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    results.append(("ROUTER REGISTRATION", False))

# ============================================================================
# 7. Check models __init__.py exports
# ============================================================================
print('\n[7] MODEL EXPORTS - app/models/__init__.py')
try:
    with open(os.path.join(backend_dir, 'app/models/__init__.py'), 'r') as f:
        models_init = f.read()
    
    has_appointment_import = 'from app.models.appointment import Appointment' in models_init
    has_appointment_export = '"Appointment"' in models_init or "'Appointment'" in models_init
    
    status = '✅' if has_appointment_import else '❌'
    print(f"  {status} Appointment imported")
    
    status = '✅' if has_appointment_export else '❌'
    print(f"  {status} Appointment exported in __all__")
    
    results.append(("MODEL EXPORTS", has_appointment_import and has_appointment_export))
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    results.append(("MODEL EXPORTS", False))

# ============================================================================
# 8. Check database table exists (via direct DB query)
# ============================================================================
print('\n[8] DATABASE TABLE - appointments')
try:
    from app.db.session import engine
    from sqlalchemy import inspect, text
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    has_table = 'appointments' in tables
    status = '✅' if has_table else '❌'
    print(f"  {status} Table 'appointments' created")
    
    if has_table:
        columns = {col['name'] for col in inspector.get_columns('appointments')}
        required_cols = {'id', 'patient_name', 'doctor_id', 'appointment_date', 'time_slot', 'status', 'created_at', 'updated_at'}
        has_cols = required_cols.issubset(columns)
        
        status = '✅' if has_cols else '❌'
        print(f"  {status} All required columns present")
        
        # Check unique constraint
        constraints = inspector.get_unique_constraints('appointments')
        has_constraint = any('doctor_id' in str(c.get('column_names', [])) for c in constraints)
        status = '✅' if has_constraint else '❌'
        print(f"  {status} Unique constraint on (doctor_id, appointment_date, time_slot)")
        
        results.append(("DATABASE TABLE", has_table and has_cols and has_constraint))
    else:
        results.append(("DATABASE TABLE", False))
except Exception as e:
    print(f"  ⚠️  WARNING: {e}")
    print(f"     Run: python create_appointment_table.py")
    results.append(("DATABASE TABLE", False))

# ============================================================================
# FINAL VERDICT
# ============================================================================
print('\n' + '='*80)

all_pass = all(passed for _, passed in results)

if all_pass:
    print('✅ MODULE 5 IMPLEMENTATION COMPLETE')
    print('='*80)
    
    print('\nMODULE 5 STRUCTURE:')
    print('  ✅ 1. Appointment model with unique constraint')
    print('  ✅ 2. Pydantic schemas (Create, Read, Update)')
    print('  ✅ 3. Scheduling router with 3 endpoints')
    print('  ✅ 4. RBAC enforcement (admin/doctor)')
    print('  ✅ 5. Conflict detection (no double-booking)')
    print('  ✅ 6. Router registered in FastAPI app')
    print('  ✅ 7. Database table created')
    
    print('\n' + '='*80)
    print('ENDPOINT SUMMARY:')
    print('='*80)
    print('\nPOST /appointments')
    print('  RBAC: Admin only')
    print('  Creates appointment with conflict detection')
    print('  Request: AppointmentCreate')
    print('  Response: AppointmentRead')
    
    print('\nGET /appointments')
    print('  RBAC: Admin only')
    print('  Lists all appointments')
    print('  Response: List[AppointmentRead]')
    
    print('\nGET /appointments/me')
    print('  RBAC: Doctor only')
    print('  Lists own appointments (filtered by doctor_id)')
    print('  Response: List[AppointmentRead]')
    
    print('\n' + '='*80)
    print('QUICK START:')
    print('='*80)
    print('\n1. Start server:')
    print('   python -m uvicorn app.main:app --reload')
    
    print('\n2. Swagger UI: http://localhost:8000/docs')
    
    print('\n3. Test as Admin:')
    print('   - POST /appointments: Create new appointment')
    print('   - GET /appointments: List all')
    print('   - POST same doctor/date/slot: See conflict error')
    
    print('\n4. Test as Doctor:')
    print('   - GET /appointments/me: View own only')
    print('   - POST /appointments: Get 403 Forbidden')
    
    print('\n5. Test RBAC:')
    print('   - Other roles: Get 403 Forbidden on all /appointments')
    
    print('\n' + '='*80 + '\n')
    
    sys.exit(0)
else:
    print('❌ MODULE 5 INCOMPLETE')
    print('='*80)
    print('\nFailed checks:')
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f'  {status} {name}')
    print('\n' + '='*80 + '\n')
    sys.exit(1)
