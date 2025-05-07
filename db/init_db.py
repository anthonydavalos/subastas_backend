#!/usr/bin/env python
"""
Script para crear todas las tablas definidas en app.models
USO:
  python db/init_db.py
"""

from db.database import Base, engine

# Importar **todos** los módulos con tus modelos ORM
import app.models.user
import app.models.vehicle
import app.models.auction
import app.models.bid
import app.models.favorite

def init_db():
    """
    Crea las tablas en la base de datos si no existen.
    checkfirst=True es implícito por defecto (no recrea tablas existentes). 
    """
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)  # crea tablas según MetaData registrada
    print("Tablas creadas correctamente.")

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada.")
    # Si se ejecuta directamente, inicializa la base de datos
