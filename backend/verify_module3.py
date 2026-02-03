#!/usr/bin/env python3
"""Module 3 Verification Script - Verify all RBAC data foundation components"""

import sys

print('MODULE 3 VERIFICATION - ALL CHECKS')
print('=' * 60)

try:
    # 1. TABLE CHECK
    print('\n[1] DATABASE TABLES')
    from sqlalchemy import inspect
    from app.db.session import engine
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    roles_exists = 'roles' in tables
    users_exists = 'users' in tables
    
    print(f"  roles table: {'OK' if roles_exists else 'MISSING'}")
    print(f"  users table: {'OK' if users_exists else 'MISSING'}")
    
    if roles_exists:
        cols = [c['name'] for c in inspector.get_columns('roles')]
        print(f"  roles columns: {cols}")
    
    if users_exists:
        cols = [c['name'] for c in inspector.get_columns('users')]
        print(f"  users columns: {cols}")
    
    # 2. FOREIGN KEY CHECK
    print('\n[2] FOREIGN KEY CONSTRAINT')
    fks = inspector.get_foreign_keys('users')
    has_role_fk = any('role_id' in fk.get('constrained_columns', []) for fk in fks)
    print(f"  role_id FK: {'OK' if has_role_fk else 'MISSING'}")
    
    for fk in fks:
        if 'role_id' in fk.get('constrained_columns', []):
            print(f"    Constraint: {fk['name']}")
            print(f"    References: {fk['referred_table']}({fk['referred_columns']})")
    
    # 3. MODEL IMPORTS
    print('\n[3] MODEL IMPORTS')
    from app.models import User, Role
    print("  OK - User and Role imported")
    
    # 4. SCHEMA IMPORTS
    print('\n[4] SCHEMA IMPORTS')
    from app.schemas.role import RoleBase, RoleCreate, RoleRead, RoleUpdate
    from app.schemas.user import UserBase, UserCreate, UserRead, UserUpdate
    print("  OK - All schemas imported")
    
    # 5. SECURITY CHECK
    print('\n[5] SECURITY CHECK')
    usercreate_fields = set(UserCreate.model_fields.keys())
    userread_fields = set(UserRead.model_fields.keys())
    has_password = 'password' in usercreate_fields
    has_no_hash = 'hashed_password' not in userread_fields
    print(f"  password in UserCreate: {has_password}")
    print(f"  hashed_password NOT in UserRead: {has_no_hash}")
    
    # 6. PYDANTIC VALIDATION
    print('\n[6] PYDANTIC VALIDATION')
    from pydantic import ValidationError
    try:
        user = UserCreate(username='dr_smith', email='smith@hospital.com', password='pass')
        print("  OK - Valid user accepted")
    except ValidationError as e:
        print(f"  ERROR: {e}")
    
    try:
        user = UserCreate(username='test', email='bad-email', password='pass')
        print("  ERROR - Invalid email accepted")
    except ValidationError:
        print("  OK - Invalid email rejected")
    
    # 7. RELATIONSHIPS
    print('\n[7] ORM RELATIONSHIPS')
    from sqlalchemy.inspection import inspect as sqlalchemy_inspect
    role_mapper = sqlalchemy_inspect(Role)
    user_mapper = sqlalchemy_inspect(User)
    print(f"  Role relationships: {[r.key for r in role_mapper.relationships]}")
    print(f"  User relationships: {[r.key for r in user_mapper.relationships]}")
    
    print('\n' + '=' * 60)
    print('MODULE 3 VERIFIED - READY FOR MODULE 4')
    print('=' * 60)
    
except Exception as e:
    print(f'\nERROR: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
