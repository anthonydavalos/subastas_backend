from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.favorite import Favorite
from app.schemas.favorite_schema import FavoriteCreate, FavoriteRead

def get_favorite(db: Session, favorite_id: int) -> Optional[Favorite]:
    return db.query(Favorite).filter(Favorite.id == favorite_id).first()

def list_favorites_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Favorite]:
    return (
        db.query(Favorite)
        .filter(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_favorite(db: Session, fav_in: FavoriteCreate) -> Favorite:
    # Opcional: comprobar si ya existe para evitar duplicados
    existing = (
        db.query(Favorite)
        .filter(
            Favorite.user_id == fav_in.user_id,
            Favorite.auction_id == fav_in.auction_id
        )
        .first()
    )
    if existing:
        return existing

    db_fav = Favorite(**fav_in.model_dump())
    db.add(db_fav)
    db.commit()
    db.refresh(db_fav)
    return db_fav

def delete_favorite(db: Session, favorite_id: int) -> bool:
    db_fav = get_favorite(db, favorite_id)
    if not db_fav:
        return False
    db.delete(db_fav)
    db.commit()
    return True
