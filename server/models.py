"""
SQLAlchemy database models.
These represent the actual database tables.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
import enum
from .database import Base


class ComponentType(str, enum.Enum):
    """Aerospace component types."""
    FUSELAGE = "fuselage"
    WING = "wing"
    ENGINE = "engine"
    LANDING_GEAR = "landing_gear"
    AVIONICS = "avionics"
    OTHER = "other"


class ComponentModel(Base):
    """
    Database model for aerospace components.
    
    Attributes:
        id: Primary key
        name: Component name
        description: Component description
        component_type: Type of component (enum)
        weight_kg: Component weight in kilograms
        material: Material composition
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    component_type = Column(SQLEnum(ComponentType), nullable=False, index=True)
    weight_kg = Column(Float, nullable=False)
    material = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self):
        return (
            f"<ComponentModel(id={self.id}, name={self.name}, "
            f"type={self.component_type}, weight={self.weight_kg}kg)>"
        )
