import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# 1) Asegúrate de que la ruta de tu proyecto esté en sys.path
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from db.database import Base, get_db
import app.models.user
import app.models.vehicle
import app.models.auction
import app.models.bid
import app.models.favorite

from main import app

# 2) URL de prueba: SQLite en memoria, StaticPool para reutilizar la conexión
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# 3) SessionLocal de testing
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 4) Crea todas las tablas en el engine de pruebas
Base.metadata.create_all(bind=engine)

# 5) Override para get_db: cede una sesión de testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 6) Aplica el override en tu app de FastAPI
app.dependency_overrides[get_db] = override_get_db

# 7) Fixture que expone TestClient usando la app configurada
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# 8) Fixture que expone directamente la sesión DB (opcional)
@pytest.fixture(scope="function")
def db_session():
    """Proporciona una sesión SQLAlchemy limpia por test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
