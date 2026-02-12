"""
Database connection and ORM models for time-series biosignal storage.

Implements async database interface using SQLAlchemy with PostgreSQL
and TimescaleDB for efficient time-series data management.

Author: Dr. Maya Anderson
Date: 2024-01-21
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, Float, String, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from databases import Database

from .config import settings


# Database instance
database = Database(str(settings.DATABASE_URL))

# Async engine for SQLAlchemy
engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=40
)

# Async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for ORM models
Base = declarative_base()


class Subject(Base):
    """Subject/participant model for tracking individuals.
    
    Attributes:
        id: Unique subject identifier
        external_id: External system identifier (e.g., hospital ID)
        name: Subject name
        age: Age in years
        weight_kg: Body weight in kilograms
        height_cm: Height in centimeters
        baseline_hr: Resting heart rate baseline
        created_at: Record creation timestamp
        active: Whether subject is currently active in system
    """
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)
    name = Column(String)
    age = Column(Integer)
    weight_kg = Column(Float)
    height_cm = Column(Float)
    baseline_hr = Column(Float, default=70.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)


class BiosignalMeasurement(Base):
    """Time-series biosignal measurements from wearable devices.
    
    Optimized for TimescaleDB hypertable partitioning on timestamp.
    """
    __tablename__ = "biosignal_measurements"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, index=True)
    timestamp = Column(DateTime, index=True, nullable=False)
    heart_rate = Column(Float)
    respiratory_rate = Column(Float)
    spo2 = Column(Float)
    temperature = Column(Float)
    accel_x = Column(Float)
    accel_y = Column(Float)
    accel_z = Column(Float)
    device_id = Column(String, index=True)
    metadata = Column(JSON)


class PoseEstimate(Base):
    """Visual pose estimation results from edge nodes.
    
    Stores keypoint coordinates and activity classifications.
    """
    __tablename__ = "pose_estimates"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, index=True)
    timestamp = Column(DateTime, index=True, nullable=False)
    keypoints = Column(JSON)  # 17x3 keypoint array
    activity_label = Column(String)
    activity_confidence = Column(Float)
    edge_node_id = Column(String, index=True)
    inference_latency_ms = Column(Float)
    metadata = Column(JSON)


class PhysiologicalStateEstimate(Base):
    """Fused physiological state estimates from Bayesian fusion.
    
    Contains probabilistic state estimates with uncertainty quantification.
    """
    __tablename__ = "physiological_states"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, index=True)
    timestamp = Column(DateTime, index=True, nullable=False)
    heart_rate = Column(Float)
    respiratory_rate = Column(Float)
    activity_level = Column(Float)
    fatigue_index = Column(Float)
    stress_level = Column(Float)
    resilience_score = Column(Float)
    covariance_matrix = Column(JSON)
    source_modalities = Column(JSON)  # List of contributing sensors
    confidence = Column(Float)


async def get_db() -> AsyncSession:
    """Dependency for getting async database session.
    
    Example:
        @app.get("/subjects/{subject_id}")
        async def get_subject(subject_id: int, db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Subject).where(Subject.id == subject_id))
            return result.scalar_one_or_none()
    """
    async with async_session() as session:
        yield session


async def init_db():
    """Initialize database schema and TimescaleDB hypertables."""
    pass


async def create_timescale_hypertables():
    """Convert time-series tables to TimescaleDB hypertables for optimization."""
    pass
