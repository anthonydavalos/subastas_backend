from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user_schema import UserCreate, UserRead
from app.crud.user_crud import (
    get_user, list_users,
    create_user, update_user, delete_user
)
from db.database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def add_user(user_in: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_in)

@router.put("/{user_id}", response_model=UserRead)
def edit_user(user_id: int, user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id, user_in)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: int, db: Session = Depends(get_db)):
    if not delete_user(db, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
