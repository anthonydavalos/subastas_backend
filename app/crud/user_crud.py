from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
from passlib.context import CryptContext

# Contexto de Passlib para hashing de contraseñas con Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def list_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_in: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    # Actualizar solo los campos enviados
    for field, value in user_in.dict(exclude_unset=True).items():
        if field == "password":
            setattr(db_user, "password_hash", pwd_context.hash(value))
        else:
            setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True
