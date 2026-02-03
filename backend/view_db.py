"""View database tables and schema"""
from sqlalchemy import inspect
from app.db.session import engine

try:
    inspector = inspect(engine)
    
    print("=" * 60)
    print("Database: hospital_workflow")
    print("=" * 60)
    
    tables = inspector.get_table_names()
    if not tables:
        print("\nNo tables yet (ready for schema)")
    else:
        print(f"\nTables ({len(tables)}):")
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"\n  {table}:")
            for col in columns:
                print(f"    - {col['name']}: {col['type']}")
    
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"ERROR: {e}")
