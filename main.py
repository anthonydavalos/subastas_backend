from fastapi import FastAPI

app = FastAPI()

@app.get("/", status_code=200)
def read_root():
    return {"message": "¡API Subastas funcionando correctamente!"}

# luego tus imports e include_router…
from app.api.users     import router as users_router
from app.api.vehicles  import router as vehicles_router
from app.api.auctions  import router as auctions_router
from app.api.bids      import router as bids_router
from app.api.favorites import router as favorites_router

app.include_router(users_router)
app.include_router(vehicles_router)
app.include_router(auctions_router)
app.include_router(bids_router)
app.include_router(favorites_router)
