# app/schemas/vehicle_schema.py

from pydantic import BaseModel, Field
from typing import Optional

class VehicleBase(BaseModel):
    brand: Optional[str] = Field(None, example="Toyota")
    model: Optional[str] = Field(None, example="Hilux")
    year: Optional[int] = Field(None, ge=1900, le=2100, example=2023)

    class Config:
        from_attributes = True

class VehicleCreate(VehicleBase):
    # Para crear, puedes requerir algunos campos si quieres,
    # pero con estos defaults Life is easy.
    external_id: int
    pass

class VehicleUpdate(VehicleBase):
    # Exactamente igual que VehicleBase: todos fields opcionales
    pass

class VehicleRead(VehicleBase):
    id: int
    category: Optional[str] = None
    subcategory: Optional[str] = None
    mileage: Optional[int] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    location_country: Optional[str] = None

    class Config:
        from_attributes = True
