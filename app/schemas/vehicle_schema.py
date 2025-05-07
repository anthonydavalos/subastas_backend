# app/schemas/vehicle_schema.py

from pydantic import BaseModel
from typing import Optional

class VehicleBase(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None

class VehicleCreate(VehicleBase):
    # Para crear, puedes requerir algunos campos si quieres,
    # pero con estos defaults Life is easy.
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
