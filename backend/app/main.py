from fastapi import FastAPI
from app.core.config import settings
from app.core.db import engine, Base
from app.scheduling import router as scheduling_router
from app.rooms import router as rooms_router
from app.shifts import router as shifts_router

# Create tables on startup (for dev/demo purposes)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Backend for hospital workflow automation (non-clinical) with AI/ML foundations.",
    version="0.1.0",
)

app.include_router(scheduling_router.router, prefix="/appointments", tags=["appointments"])
app.include_router(rooms_router.router, prefix="/rooms", tags=["rooms"])
app.include_router(shifts_router.router, prefix="/shifts", tags=["shifts"])


@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "Hospital Workflow Backend Running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
