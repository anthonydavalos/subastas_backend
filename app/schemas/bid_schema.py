# app/schemas/bid_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BidBase(BaseModel):
    auction_id: int
    user_id: int
    amount: float

    class Config:
        from_attributes = True

class BidCreate(BidBase):
    """Datos para crear una puja."""
    amount: float

class BidRead(BidBase):
    """Esquema de respuesta de una puja."""
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
