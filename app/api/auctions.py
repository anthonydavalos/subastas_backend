# en app/api/auctions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.auction_schema import AuctionCreate, AuctionRead
from app.crud.auction_crud import (
    get_auction, list_auctions,
    create_auction, update_auction, delete_auction
)
from db.database import get_db

router = APIRouter(prefix="/auctions", tags=["auctions"])

@router.get("/auctions/", response_model=List[AuctionRead])
def read_auctions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_auctions(db, skip, limit)

@router.get("/{auction_id}", response_model=AuctionRead)
def read_auction(auction_id: int, db: Session = Depends(get_db)):
    db_auction = get_auction(db, auction_id)
    if not db_auction:
        raise HTTPException(404, "Auction not found")
    return db_auction

@router.post("/", response_model=AuctionRead)
def add_auction(auction_in: AuctionCreate, db: Session = Depends(get_db)):
    return create_auction(db, auction_in)

@router.put("/{auction_id}", response_model=AuctionRead)
def edit_auction(auction_id: int, auction_in: AuctionCreate, db: Session = Depends(get_db)):
    db_auction = update_auction(db, auction_id, auction_in)
    if not db_auction:
        raise HTTPException(404, "Auction not found")
    return db_auction

@router.delete("/{auction_id}", status_code=204)
def remove_auction(auction_id: int, db: Session = Depends(get_db)):
    if not delete_auction(db, auction_id):
        raise HTTPException(404, "Auction not found")
