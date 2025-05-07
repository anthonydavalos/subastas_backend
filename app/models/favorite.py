from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from db.database import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    auction_id   = Column(Integer, ForeignKey("auctions.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relaciones
    user         = relationship("User", back_populates="favorites")
    auction      = relationship("Auction", back_populates="favorites")
