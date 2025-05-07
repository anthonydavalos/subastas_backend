# app/schemas/auction_schema.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AuctionBase(BaseModel):
    source: str = Field(..., example="superbid")
    external_id: int = Field(..., example=3800748)
    lot_number: Optional[int] = Field(None, example=1)
    title: Optional[str] = Field(None, example="Toyota Hilux 2023")
    description: Optional[str] = Field(None)
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    base_price: Optional[float]
    current_price: Optional[float]
    currency: Optional[str] = Field(None, example="USD")
    visits: Optional[int] = Field(None, example=809)
    total_bidders: Optional[int] = Field(None, example=5)
    total_bids: Optional[int] = Field(None, example=12)
    reserved_price: Optional[float] = Field(None, example=999999.0)
    bid_increment: Optional[float] = Field(None, example=50.0)
    vehicle_id: Optional[int]
    seller_name: Optional[str] = Field(None, example="La Positiva")
    seller_company: Optional[str] = Field(None, example="La Positiva Seguros")

    class Config:
        from_attributes = True

class AuctionCreate(AuctionBase):
    """Campos requeridos para crear una subasta."""
    source: str
    external_id: int
    start_time: datetime
    end_time: datetime
    base_price: float
    current_price: float
    vehicle_id: int

class AuctionRead(AuctionBase):
    """Respuesta al obtener subastas."""
    id: int

    class Config:
        from_attributes = True
