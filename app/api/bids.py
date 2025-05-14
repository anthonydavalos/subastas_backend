from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.bid_schema import BidCreate, BidRead
from app.crud.bid_crud import (
    get_bid,
    list_bids_for_auction,
    create_bid,
    delete_bid,
)
from db.database import get_db

router = APIRouter(prefix="/bids", tags=["bids"])

@router.get("/auction/{auction_id}", response_model=List[BidRead])
def read_bids_for_auction(
    auction_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Lista las pujas de una subasta dada.
    """
    return list_bids_for_auction(db, auction_id, skip, limit)

@router.get("/{bid_id}", response_model=BidRead)
def read_bid(
    bid_id: int,
    db: Session = Depends(get_db),
):
    """
    Obtiene una puja por su ID.
    """
    db_bid = get_bid(db, bid_id)
    if not db_bid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bid not found")
    return db_bid

@router.post("/", response_model=BidRead, status_code=status.HTTP_201_CREATED)
def add_bid(
    bid_in: BidCreate,
    db: Session = Depends(get_db),
):
    """
    Crea una nueva puja.
    """
    return create_bid(db, bid_in)

@router.delete("/{bid_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_bid(
    bid_id: int,
    db: Session = Depends(get_db),
):
    """
    Elimina una puja por su ID.
    """
    success = delete_bid(db, bid_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bid not found")
