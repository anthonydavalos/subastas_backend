from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id             = Column(Integer, primary_key=True, index=True)
    username       = Column(String(50), unique=True, nullable=False, index=True)
    email          = Column(String(120), unique=True, nullable=False, index=True)
    password_hash  = Column(String(128), nullable=False)
    role           = Column(String(20), default="user", nullable=False)
    created_at     = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relaciones
    bids           = relationship("Bid", back_populates="user", cascade="all, delete-orphan")
    favorites      = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
