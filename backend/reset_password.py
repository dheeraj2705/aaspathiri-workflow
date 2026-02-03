"""Reset backend_user password to match .env"""
import psycopg2
from psycopg2 import sql

try:
    # Connect as postgres superuser
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="postgres",
        database="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Reset backend_user password
    new_password = "strong_backend_password_2024"
    cursor.execute(
        sql.SQL("ALTER USER backend_user WITH PASSWORD %s;"),
        [new_password]
    )
    print(f"OK: Reset backend_user password to: {new_password}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"ERROR: {e}")
