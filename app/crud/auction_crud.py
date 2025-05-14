from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.auction import Auction
from app.schemas.auction_schema import AuctionCreate, AuctionRead

def get_auction(db: Session, auction_id: int) -> Optional[Auction]:
    return db.query(Auction).filter(Auction.id == auction_id).first()

def list_auctions(db: Session, skip: int = 0, limit: int = 100) -> List[Auction]:
    return db.query(Auction).offset(skip).limit(limit).all()

def create_auction(db: Session, auction_in: AuctionCreate) -> Auction:
    db_auction = Auction(**auction_in.model_dump())
    db.add(db_auction)
    db.commit()
    db.refresh(db_auction)
    return db_auction

def update_auction(db: Session, auction_id: int, auction_in: AuctionCreate) -> Optional[Auction]:
    db_auction = get_auction(db, auction_id)
    if not db_auction:
        return None
    for field, value in auction_in.dict(exclude_unset=True).items():
        setattr(db_auction, field, value)
    db.commit()
    db.refresh(db_auction)
    return db_auction

def delete_auction(db: Session, auction_id: int) -> bool:
    db_auction = get_auction(db, auction_id)
    if not db_auction:
        return False
    db.delete(db_auction)
    db.commit()
    return True

def get_auction_by_external_id(db: Session, external_id: int) -> Optional[Auction]:
    return db.query(Auction).filter(Auction.external_id == external_id).first()
