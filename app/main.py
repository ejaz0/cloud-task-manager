import structlog
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import settings
from app.core.logging_config import setup_logging

setup_logging()
logger = structlog.get_logger()

from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
)

# Include v1 router
app.include_router(api_router, prefix="/api/v1")

# Instrument Prometheus
Instrumentator().instrument(app).expose(app)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up CloudTask API")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down CloudTask API")
