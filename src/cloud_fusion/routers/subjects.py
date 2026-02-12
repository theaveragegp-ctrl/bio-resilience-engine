"""
API router for subject/participant management.

Author: Dr. Maya Anderson
Date: 2024-01-22
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db, Subject


router = APIRouter()


class SubjectCreate(BaseModel):
    """Request model for creating new subject."""
    external_id: str = Field(..., description="External system identifier")
    name: str
    age: int = Field(..., ge=18, le=100)
    weight_kg: float = Field(..., ge=30, le=300)
    height_cm: float = Field(..., ge=100, le=250)
    baseline_hr: Optional[float] = Field(70.0, ge=40, le=100)


class SubjectResponse(BaseModel):
    """Response model for subject data."""
    id: int
    external_id: str
    name: str
    age: int
    weight_kg: float
    height_cm: float
    baseline_hr: float
    created_at: datetime
    active: bool
    
    class Config:
        from_attributes = True


@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(
    subject: SubjectCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register new subject in the system.
    
    Args:
        subject: Subject registration data
        db: Database session
        
    Returns:
        Created subject record
    """
    pass


@router.get("/{subject_id}", response_model=SubjectResponse)
async def get_subject(
    subject_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve subject by ID.
    
    Args:
        subject_id: Subject database ID
        db: Database session
        
    Returns:
        Subject record
    """
    pass


@router.get("/", response_model=List[SubjectResponse])
async def list_subjects(
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all subjects with pagination.
    
    Args:
        active_only: Filter for active subjects only
        skip: Number of records to skip
        limit: Maximum records to return
        db: Database session
        
    Returns:
        List of subjects
    """
    pass
