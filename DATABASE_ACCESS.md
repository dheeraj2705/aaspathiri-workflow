# Hospital Workflow Backend - Database Setup

## Database Status ✅
- **Status**: Configured and Ready
- **Database**: `hospital_workflow`
- **Tables**: 0 (ready for schema)
- **Users**: 1 (backend_user)

---

## Connection Details (Share with Team)

### PostgreSQL Server
| Property | Value |
|----------|-------|
| **Host** | `10.12.119.203` |
| **Port** | `5432` |
| **Database** | `hospital_workflow` |
| **User** | `backend_user` |
| **Password** | `strong_backend_password_2024` |

---

## How Each Developer Connects

### 1️⃣ Via FastAPI (Recommended)
Start the backend from your machine:
```powershell
Set-Location 'E:\Hospital_Workflow\aaspathiri-workflow\backend'
& 'E:\Hospital_Workflow\env\Scripts\python.exe' -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then access:
- **Swagger UI (API docs)**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health
- **DB health**: http://localhost:8000/db/health

### 2️⃣ Via Python Script
From the backend directory:
```powershell
Set-Location 'E:\Hospital_Workflow\aaspathiri-workflow\backend'
$env:PYTHONPATH='E:\Hospital_Workflow\aaspathiri-workflow\backend'
& 'E:\Hospital_Workflow\env\Scripts\python.exe' view_db.py
```

Outputs:
```
============================================================
Database: hospital_workflow
============================================================

No tables yet (ready for schema)

============================================================
```

### 3️⃣ Via Python (psycopg2)
```python
import psycopg2

conn = psycopg2.connect(
    host="10.12.119.203",
    user="backend_user",
    password="strong_backend_password_2024",
    database="hospital_workflow",
    port=5432
)
cursor = conn.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())
cursor.close()
conn.close()
```

### 4️⃣ Via pgAdmin or DBeaver (GUI)
Create a new PostgreSQL connection:
- **Server**: `10.12.119.203`
- **Port**: `5432`
- **Database**: `hospital_workflow`
- **Username**: `backend_user`
- **Password**: `strong_backend_password_2024`

---

## View Database Structure
```powershell
Set-Location 'E:\Hospital_Workflow\aaspathiri-workflow\backend'
$env:PYTHONPATH='E:\Hospital_Workflow\aaspathiri-workflow\backend'
& 'E:\Hospital_Workflow\env\Scripts\python.exe' view_db.py
```

---

## Environment Variables (.env)
All developers should have these in `backend/.env`:
```
POSTGRES_USER=backend_user
POSTGRES_PASSWORD=strong_backend_password_2024
POSTGRES_DB=hospital_workflow
POSTGRES_HOST=10.12.119.203
POSTGRES_PORT=5432
```

---

## Security Notes
⚠️ **Before Production:**
1. Rotate `POSTGRES_PASSWORD` and store in a vault (AWS Secrets Manager, Azure KeyVault, etc.)
2. Restrict `pg_hba.conf` to allow only team IP ranges (not `0.0.0.0/0`)
3. Use SSH tunnels instead of exposing port 5432 directly:
   ```bash
   ssh -L 5432:localhost:5432 user@10.12.119.203
   ```
   Then use `POSTGRES_HOST=localhost` in `.env`

---

## Next Steps
- Create database schema (tables, indexes, constraints)
- Add Alembic for schema migrations
- Create ORM models in `backend/app/models/`
- Build API endpoints to query the database

---

**Questions?** Reach out to the DB owner at [your contact].
