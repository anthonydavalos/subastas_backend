from fastapi import FastAPI
from db.database import engine, Base
from app.api import users, vehicles, auctions, bids, favorites

# Crea todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Instancia principal de FastAPI
app = FastAPI(
    title="Subastas Vehiculares API",
    description="API backend para gestionar subastas de vehículos",
    version="1.0.0",
)

# Incluir routers (endpoints organizados por módulos)
# app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(vehicles.router, prefix="/vehicles", tags=["Vehicles"])
app.include_router(auctions.router, prefix="/auctions", tags=["Auctions"])
app.include_router(bids.router, prefix="/bids", tags=["Bids"])
app.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])

# Endpoint raíz (opcional)
@app.get("/")
def read_root():
    return {"message": "🚗 Bienvenido a la API de Subastas Vehiculares"}
