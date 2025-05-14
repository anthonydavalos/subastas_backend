from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from db.database import Base
from app.models.user import User

class Bid(Base):
    __tablename__ = "bids"

    id           = Column(Integer, primary_key=True, index=True)
    auction_id   = Column(Integer, ForeignKey("auctions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id      = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    amount       = Column(Float, nullable=False)
    timestamp    = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relaciones
    auction      = relationship("Auction", back_populates="bids")
    user         = relationship(User, back_populates="bids")