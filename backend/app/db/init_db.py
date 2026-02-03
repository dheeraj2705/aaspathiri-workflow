"""Initialize database tables.

This script creates all SQLAlchemy models defined in app.models
into the PostgreSQL database.

Usage:
    python -m app.db.init_db
    
    or from Python:
    from app.db.init_db import init_db
    init_db()
"""
from app.db.base import Base
from app.db.session import engine
from app.models import Role, User  # Import all models to register them


def init_db() -> None:
    """Create all tables defined in Base.metadata."""
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("[OK] Tables created successfully!")
    print("\nCreated tables:")
    print("  - roles")
    print("  - users")
    print("\nNext steps:")
    print("  1. Verify tables exist: SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    print("  2. Insert test data via SQL or a seeding script")
    print("  3. Proceed with Module 4 (Authentication)")


if __name__ == "__main__":
    init_db()
