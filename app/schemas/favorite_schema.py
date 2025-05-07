# app/schemas/favorite_schema.py
from pydantic import BaseModel
from datetime import datetime

class FavoriteBase(BaseModel):
    user_id: int
    auction_id: int

    class Config:
        from_attributes = True

class FavoriteCreate(FavoriteBase):
    """Campos para marcar una subasta como favorita."""
    pass

class FavoriteRead(FavoriteBase):
    """Respuesta al obtener favoritos."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
