from fastapi import FastAPI

# Central FastAPI application instance; routers will be added as modules mature.
app = FastAPI(
    title="Hospital Workflow Automation Portal",
    description="Backend for hospital workflow automation (non-clinical) with AI/ML foundations.",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "Hospital Workflow Backend Running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
