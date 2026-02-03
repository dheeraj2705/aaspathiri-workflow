"""Test psql connection with backend_user"""
import psycopg2

try:
    conn = psycopg2.connect(
        host="10.12.119.203",
        user="backend_user",
        password="strong_backend_password_2024",
        database="hospital_workflow",
        port=5432
    )
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"OK: Connected to PostgreSQL: {version[0][:50]}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
