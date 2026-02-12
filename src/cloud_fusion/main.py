"""
FastAPI backend for Bio-Resilience Engine cloud fusion service.

Implements RESTful API for biosignal ingestion, Bayesian sensor fusion,
and physiological resilience analysis. Integrates with PostgreSQL for
time-series storage and Redis for real-time caching.

Author: Dr. Maya Anderson
Date: 2024-01-22
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
import structlog

from .config import settings
from .database import database, engine
from .routers import fusion, analysis, subjects, health
from .mqtt_subscriber import MQTTSubscriber


# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan manager for startup/shutdown events.
    
    Handles database connections, MQTT subscriber initialization,
    and graceful shutdown procedures.
    """
    # Startup
    logger.info("Starting Bio-Resilience Engine Cloud Fusion API")
    
    # Connect to database
    await database.connect()
    logger.info("Database connection established")
    
    # Initialize MQTT subscriber for edge data ingestion
    mqtt_subscriber = MQTTSubscriber(
        broker=settings.MQTT_BROKER,
        topics=["bio-resilience/edge/+/pose", "bio-resilience/edge/+/activity"]
    )
    await mqtt_subscriber.start()
    logger.info("MQTT subscriber started")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Cloud Fusion API")
    await mqtt_subscriber.stop()
    await database.disconnect()
    logger.info("Shutdown complete")


# Initialize FastAPI application
app = FastAPI(
    title="Bio-Resilience Engine API",
    description="Cloud fusion backend for multi-modal physiological monitoring",
    version="0.4.2",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)


# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


# Include API routers
app.include_router(
    fusion.router,
    prefix="/api/v1/fusion",
    tags=["Sensor Fusion"]
)

app.include_router(
    analysis.router,
    prefix="/api/v1/analysis",
    tags=["Physiological Analysis"]
)

app.include_router(
    subjects.router,
    prefix="/api/v1/subjects",
    tags=["Subject Management"]
)

app.include_router(
    health.router,
    prefix="/api/v1/health",
    tags=["Health & Status"]
)


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Bio-Resilience Engine API",
        "version": "0.4.2",
        "status": "operational",
        "docs": "/api/docs"
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler with structured logging."""
    logger.error(
        "HTTP exception",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
