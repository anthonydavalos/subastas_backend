# app/models/auction.py

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, JSON, ForeignKey
)
from app.models.bid import Bid
from app.models.favorite import Favorite
from sqlalchemy.orm import relationship
from db.database import Base
import datetime

class Auction(Base):
    __tablename__ = "auctions"

    id                    = Column(Integer, primary_key=True, index=True)
    source                = Column(String, nullable=False)      # e.g. "superbid"
    external_id           = Column(Integer, nullable=False, index=True)
    lot_number            = Column(Integer)
    title                 = Column(String(256))
    description           = Column(String)
    start_time            = Column(DateTime)
    end_time              = Column(DateTime)

    base_price            = Column(Float)
    current_price         = Column(Float)
    currency              = Column(String(10))

    visits                = Column(Integer)
    total_bidders         = Column(Integer)
    total_bids            = Column(Integer)

    reserved_price        = Column(Float)
    bid_increment         = Column(Float)

    # Campos para estadísticas finales
    final_total_bidders   = Column(Integer, nullable=True)
    final_total_bids      = Column(Integer, nullable=True)

    # Fecha de la última sincronización
    last_synced           = Column(
                              DateTime,
                              nullable=True,
                              default=lambda: datetime.datetime.utcnow()
                          )

    vehicle_id            = Column(
                              Integer,
                              ForeignKey("vehicles.id", ondelete="SET NULL"),
                              nullable=True
                          )
    seller_name           = Column(String(128))
    seller_company        = Column(String(128))

    images                = Column(JSON)   # ["url1", "url2", …]
    attachments           = Column(JSON)   # [{"file":"ipf…","url":"…"}, …]

    # Relaciones
    vehicle               = relationship(
                              "Vehicle",
                              back_populates="auctions"
                          )
    bids                  = relationship(Bid, back_populates="auction")
    favorites             = relationship(Favorite, back_populates="auction")
