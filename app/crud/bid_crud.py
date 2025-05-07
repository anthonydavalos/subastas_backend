from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.bid import Bid
from app.schemas.bid_schema import BidCreate, BidRead

def get_bid(db: Session, bid_id: int) -> Optional[Bid]:
    return db.query(Bid).filter(Bid.id == bid_id).first()

def list_bids_for_auction(db: Session, auction_id: int, skip: int = 0, limit: int = 100) -> List[Bid]:
    return (
        db.query(Bid)
        .filter(Bid.auction_id == auction_id)
        .order_by(Bid.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_bid(db: Session, bid_in: BidCreate) -> Bid:
    db_bid = Bid(**bid_in.dict())
    db.add(db_bid)
    db.commit()
    db.refresh(db_bid)
    return db_bid

def delete_bid(db: Session, bid_id: int) -> bool:
    db_bid = get_bid(db, bid_id)
    if not db_bid:
        return False
    db.delete(db_bid)
    db.commit()
    return True
