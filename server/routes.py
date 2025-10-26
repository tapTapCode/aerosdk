"""
FastAPI routes for component management.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from server.database import get_db
from server.models import ComponentModel, ComponentType
from sdk.models import Component, ComponentCreate, ComponentUpdate

router = APIRouter(prefix="/api/components", tags=["components"])


@router.get("", response_model=List[Component])
def list_components(
    component_type: Optional[str] = Query(None, description="Filter by component type"),
    db: Session = Depends(get_db),
):
    """
    Get all components, optionally filtered by type.
    
    Query Parameters:
        component_type: Optional filter by component type (e.g., "wing", "engine")
    """
    query = db.query(ComponentModel)
    
    if component_type:
        try:
            component_type_enum = ComponentType(component_type)
            query = query.filter(ComponentModel.component_type == component_type_enum)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid component type: {component_type}"
            )
    
    components = query.all()
    return components


@router.get("/{component_id}", response_model=Component)
def get_component(component_id: int, db: Session = Depends(get_db)):
    """Get a specific component by ID."""
    component = db.query(ComponentModel).filter(
        ComponentModel.id == component_id
    ).first()
    
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    
    return component


@router.post("", response_model=Component, status_code=201)
def create_component(
    component_data: ComponentCreate,
    db: Session = Depends(get_db),
):
    """Create a new component."""
    # Create new component model
    db_component = ComponentModel(
        name=component_data.name,
        description=component_data.description,
        component_type=component_data.component_type,
        weight_kg=component_data.weight_kg,
        material=component_data.material,
    )
    
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    
    return db_component


@router.put("/{component_id}", response_model=Component)
def update_component(
    component_id: int,
    component_data: ComponentUpdate,
    db: Session = Depends(get_db),
):
    """Update a component."""
    component = db.query(ComponentModel).filter(
        ComponentModel.id == component_id
    ).first()
    
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    
    # Update only provided fields
    update_data = component_data.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(component, field, value)
    
    db.commit()
    db.refresh(component)
    
    return component


@router.delete("/{component_id}", status_code=204)
def delete_component(component_id: int, db: Session = Depends(get_db)):
    """Delete a component."""
    component = db.query(ComponentModel).filter(
        ComponentModel.id == component_id
    ).first()
    
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    
    db.delete(component)
    db.commit()
