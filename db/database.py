from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

# Configurar conexión a la base de datos PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL no configurado en tu .env")

# Crear motor de conexión
engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=True,
    pool_pre_ping=True,
)

# Session local para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos de SQLAlchemy
metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)
Base = declarative_base(metadata=metadata)

def get_db() -> Session:
    """
    Dependencia de FastAPI que crea una sesión de DB,
    la cierra al terminar y la inyecta en los endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()