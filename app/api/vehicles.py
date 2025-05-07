from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

from app.schemas.vehicle_schema import VehicleCreate, VehicleRead, VehicleUpdate
from app.crud.vehicle_crud import (
    get_vehicle, list_vehicles,
    create_vehicle, update_vehicle, delete_vehicle
)
from db.database import get_db

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.get("/", response_model=List[VehicleRead])
def read_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_vehicles(db, skip=skip, limit=limit)

@router.get("/{vehicle_id}", response_model=VehicleRead)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = get_vehicle(db, vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return db_vehicle

@router.post("/", response_model=VehicleRead, status_code=status.HTTP_201_CREATED)
def add_vehicle(vehicle_in: VehicleCreate, db: Session = Depends(get_db)):
    return create_vehicle(db, vehicle_in)

@router.put("/{vehicle_id}", response_model=VehicleRead)
def edit_vehicle(vehicle_id: int, vehicle_in: VehicleUpdate, db: Session = Depends(get_db)):
    db_vehicle = update_vehicle(db, vehicle_id, vehicle_in)
    if not db_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return db_vehicle

@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    if not delete_vehicle(db, vehicle_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
