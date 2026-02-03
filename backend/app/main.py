from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.deps import get_db
from app.auth.router import router as auth_router
from app.scheduling.router import router as scheduling_router


# Central FastAPI application instance; routers will be added as modules mature.
app = FastAPI(
    title=settings.app_name,
    description="Backend for hospital workflow automation (non-clinical) with AI/ML foundations.",
    version="0.1.0",
    debug=settings.debug,
)

# Register routers
app.include_router(auth_router)
app.include_router(scheduling_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "Hospital Workflow Backend Running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/db/health")
def db_health(db: Session = Depends(get_db)) -> dict[str, str]:
    """Check database connectivity."""
    try:
        # Simple query to verify database connection
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}
