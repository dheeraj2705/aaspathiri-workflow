"""Find PostgreSQL config file locations."""
import psycopg2

conn = psycopg2.connect(host="localhost", user="postgres", password="postgres")
cursor = conn.cursor()

cursor.execute("SHOW config_file;")
config_file = cursor.fetchone()[0]

cursor.execute("SHOW hba_file;")
hba_file = cursor.fetchone()[0]

print(f"Config file: {config_file}")
print(f"HBA file: {hba_file}")

cursor.close()
conn.close()
