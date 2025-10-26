"""
Pydantic models for aerospace data structures.
These define the shape of data with validation rules.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ComponentType(str, Enum):
    """Aerospace component types."""
    FUSELAGE = "fuselage"
    WING = "wing"
    ENGINE = "engine"
    LANDING_GEAR = "landing_gear"
    AVIONICS = "avionics"
    OTHER = "other"


class ComponentBase(BaseModel):
    """Base component model with common fields."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    component_type: ComponentType
    weight_kg: float = Field(..., gt=0)
    material: Optional[str] = Field(None, max_length=100)


class Component(ComponentBase):
    """Full component model with ID and metadata."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ComponentCreate(ComponentBase):
    """Model for creating new components."""
    pass


class ComponentUpdate(BaseModel):
    """Model for updating component fields."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    component_type: Optional[ComponentType] = None
    weight_kg: Optional[float] = Field(None, gt=0)
    material: Optional[str] = Field(None, max_length=100)


class Assembly(BaseModel):
    """Represents an assembly of multiple components."""
    id: int
    name: str
    components: List[Component]
    total_weight_kg: float

    class Config:
        from_attributes = True


class FileUploadResponse(BaseModel):
    """Response after uploading and parsing a file."""
    file_name: str
    components_parsed: int
    success: bool
    message: str
