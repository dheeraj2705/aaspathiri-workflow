"""Grant necessary permissions to backend_user."""
import psycopg2
from psycopg2 import sql

try:
    # Connect as postgres superuser
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="postgres",
        database="hospital_workflow"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Grant permissions to backend_user
    print("Granting permissions to backend_user...")
    
    # Grant schema permissions
    cursor.execute("GRANT ALL PRIVILEGES ON SCHEMA public TO backend_user;")
    print("[OK] SCHEMA public permissions granted")
    
    # Grant table permissions (future tables)
    cursor.execute("ALTER DEFAULT PRIVILEGES FOR USER postgres IN SCHEMA public GRANT ALL ON TABLES TO backend_user;")
    print("[OK] Default table permissions set")
    
    # Grant sequence permissions
    cursor.execute("ALTER DEFAULT PRIVILEGES FOR USER postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO backend_user;")
    print("[OK] Default sequence permissions set")
    
    cursor.close()
    conn.close()
    print("\nOK: Permissions granted successfully!")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
