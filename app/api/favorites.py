from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.favorite_schema import FavoriteCreate, FavoriteRead
from app.crud.favorite_crud import (
    get_favorite,
    list_favorites_for_user,
    create_favorite,
    delete_favorite,
)
from db.database import get_db

router = APIRouter(prefix="/favorites", tags=["favorites"])

@router.get("/user/{user_id}", response_model=List[FavoriteRead])
def read_favorites_for_user(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Lista los favoritos de un usuario dado.
    """
    return list_favorites_for_user(db, user_id, skip, limit)

@router.get("/{favorite_id}", response_model=FavoriteRead)
def read_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
):
    """
    Obtiene un favorito por su ID.
    """
    db_fav = get_favorite(db, favorite_id)
    if not db_fav:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")
    return db_fav

@router.post("/", response_model=FavoriteRead, status_code=status.HTTP_201_CREATED)
def add_favorite(
    fav_in: FavoriteCreate,
    db: Session = Depends(get_db),
):
    """
    Marca una subasta como favorita para un usuario.
    """
    return create_favorite(db, fav_in)

@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
):
    """
    Elimina un favorito por su ID.
    """
    success = delete_favorite(db, favorite_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")
    return
