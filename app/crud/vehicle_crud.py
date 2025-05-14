from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.vehicle import Vehicle
from app.schemas.vehicle_schema import VehicleCreate, VehicleUpdate


def create_vehicle(db: Session, veh: VehicleCreate) -> Vehicle:
    db_veh = Vehicle(**veh.model_dump())   # Pydantic V2 usa model_dump()
    db.add(db_veh)
    db.commit()
    db.refresh(db_veh)
    return db_veh


def get_vehicle(db: Session, vehicle_id: int) -> Optional[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()


def get_vehicle_by_external_id(db: Session, external_id: int):
    """
    Busca un vehículo por su external_id y lo retorna, o None si no existe.
    """
    return db.query(Vehicle).filter(Vehicle.external_id == external_id).first()


def list_vehicles(db: Session, skip: int = 0, limit: int = 100) -> List[Vehicle]:
    return db.query(Vehicle).offset(skip).limit(limit).all()


def update_vehicle(db: Session, vehicle_id: int, veh_in: VehicleUpdate):
    db_veh = get_vehicle(db, vehicle_id)
    if not db_veh:
        return None
    update_data = veh_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_veh, field, value)
    db.commit()
    db.refresh(db_veh)
    return db_veh


def delete_vehicle(db: Session, vehicle_id: int):
    db_veh = get_vehicle(db, vehicle_id)
    if not db_veh:
        return False
    db.delete(db_veh)
    db.commit()
    return True
