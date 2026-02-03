"""Test database connection."""
from sqlalchemy import text
from app.db.session import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("OK: Database connection successful!")
except Exception as e:
    print(f"ERROR: Database connection failed: {e}")
    import traceback
    traceback.print_exc()
