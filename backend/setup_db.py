"""Setup PostgreSQL database and user for multi-developer access."""
import psycopg2
from psycopg2 import sql

try:
    # Connect to default postgres database
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="postgres",
        database="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Create database
    try:
        cursor.execute("CREATE DATABASE hospital_workflow;")
        print("✓ Created hospital_workflow database")
    except psycopg2.errors.DuplicateDatabase:
        print("⚠ Database hospital_workflow already exists")
    
    # Create user
    try:
        cursor.execute(
            sql.SQL("CREATE USER backend_user WITH PASSWORD %s;"),
            ["strong_backend_password_2024"]
        )
        print("✓ Created backend_user")
    except psycopg2.errors.DuplicateObject:
        print("⚠ User backend_user already exists")
    
    # Grant permissions
    cursor.execute("GRANT CONNECT ON DATABASE hospital_workflow TO backend_user;")
    cursor.execute("GRANT USAGE ON SCHEMA public TO backend_user;")
    cursor.execute("GRANT CREATE ON SCHEMA public TO backend_user;")
    print("✓ Granted permissions to backend_user")
    
    cursor.close()
    conn.close()
    print("\n✅ Database setup complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Make sure PostgreSQL is running and postgres password is correct")
