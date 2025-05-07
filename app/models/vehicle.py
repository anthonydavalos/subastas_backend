from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id               = Column(Integer, primary_key=True, index=True)
    brand            = Column(String(64), nullable=True)
    model            = Column(String(64), nullable=True)
    year             = Column(Integer, nullable=True)
    category         = Column(String(64), nullable=True)
    subcategory      = Column(String(64), nullable=True)
    mileage          = Column(Integer, nullable=True)
    location_city    = Column(String(64), nullable=True)
    location_state   = Column(String(64), nullable=True)
    location_country = Column(String(64), nullable=True)

    auctions = relationship(
        "Auction",
        back_populates="vehicle",
        cascade="all, delete-orphan",
        single_parent=True  # habilita delete-orphan correctamente
    )
