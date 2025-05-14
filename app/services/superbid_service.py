# app/services/superbid_service.py

import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import List

logger = logging.getLogger(__name__)

# Configuración de sesión con retries (igual que antes)
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429,502,503,504])
session.mount("https://", HTTPAdapter(max_retries=retries))
session.headers.update({
    "Accept": "application/json",
    "User-Agent": "subastas-backend/1.0",
})
session.timeout = 10

# Punto de entrada sin paginación basada en 'start'
BASE_URL = (
    "https://api.sbwebservices.net/offer-query/offers/"
    "?filter=product.subCategory.category.description:autos;"
    "product.location.city:lima;"
    "product.productType.description:autos-y-motos"
    "&locale=es_PE&orderBy=endDate:asc"
    "&portalId=21&requestOrigin=marketplace"
    "&searchType=opened&timeZoneId=America%2FLima"
)

def fetch_all_offers_raw() -> List[dict]:
    offers = []
    page = 1
    page_size = 100

    while True:
        url = f"{BASE_URL}&pageNumber={page}&pageSize={page_size}"
        resp = session.get(url)
        if resp.status_code != 200:
            logger.error("Error al descargar página %d: %d %s", 
                         page, resp.status_code, resp.text[:200])
            break

        try:
            data = resp.json()
        except ValueError:
            logger.error("Respuesta no JSON en página %d: %s", page, resp.text[:200])
            break

        batch = data.get("offers", [])
        if batch:
            logger.debug("Primera oferta: %s", batch[0])  # Agrega esto
        if not batch:
            # no hay más ofertas
            break

        offers.extend(batch)
        total = data.get("total", 0)
        logger.info("Página %d descargada: %d ofertas (total estimado %d)", 
                    page, len(batch), total)

        # si ya bajamos todas
        if len(offers) >= total:
            break

        page += 1

    logger.info("Total ofertas descargadas: %d", len(offers))
    return offers

def import_superbid_auctions():
    """
    Descarga, parsea e inserta en la BD todas las ofertas de Superbid.
    Evita duplicados y lleva conteo de registros creados.
    """
    from db.database import SessionLocal
    from app.crud.auction_crud import create_auction, get_auction_by_external_id
    from app.crud.vehicle_crud import create_vehicle, get_vehicle_by_external_id
    from app.schemas.auction_schema import AuctionCreate
    from app.schemas.vehicle_schema import VehicleCreate
    import json

    db = SessionLocal()
    raws = fetch_all_offers_raw()

    created_vehicles = 0
    created_auctions = 0

    for raw in raws:  #[:1]:  # limitar a una sola oferta para inspección
        # print(json.dumps(raw, indent=2, ensure_ascii=False))  # imprime bonito
        # break
        auction_schema, vehicle_schema = parse_offer(raw)

        # VEHICLE
        vehicle = get_vehicle_by_external_id(db, vehicle_schema.external_id)
        if not vehicle:
            vehicle = create_vehicle(db, vehicle_schema)
            created_vehicles += 1

        # Asignamos ID antes de crear la subasta
        auction_schema.vehicle_id = vehicle.id

        existing_auction = get_auction_by_external_id(db, auction_schema.external_id)
        if not existing_auction:
            create_auction(db, auction_schema)
            created_auctions += 1

    db.close()
    print(f"✅ Importación completada: {created_vehicles} vehículos nuevos, {created_auctions} subastas nuevas.")

# app/services/superbid_service.py

from app.schemas.auction_schema import AuctionCreate
from app.schemas.vehicle_schema import VehicleCreate
from typing import Tuple

from bs4 import BeautifulSoup

def parse_offer(raw: dict) -> tuple[dict, dict]:
    from datetime import datetime

    # Parsear fechas
    try:
        start_time = datetime.fromisoformat(raw["auction"]["beginDate"])
        end_time = datetime.fromisoformat(raw["endDate"])
    except Exception:
        raise ValueError("Faltan fechas obligatorias")

    # 1. Extraer texto HTML del campo de descripción
    description_html = raw.get("offerDescription", {}).get("offerDescription", "")
    soup = BeautifulSoup(description_html, "html.parser")
    description_text = soup.get_text(separator="\n")

    def extract_line(label: str) -> str | None:
        for line in description_text.splitlines():
            if label in line.upper():
                return line.split(":")[-1].strip()
        return None

    brand = extract_line("MARCA")
    model = extract_line("MODELO")
    year = extract_line("AÑO")
    license_plate = extract_line("PLACA")
    location = extract_line("UBICACIÓN")

    # Separar ciudad y distrito si es posible
    location_city, location_state = (location.split("-") + [None])[:2] if location else (None, None)

    vehicle_data = {
        "brand": brand,
        "model": model,
        "year": int(year) if year and year.isdigit() else None,
        "category": "Autos",
        "subcategory": "Siniestrado",
        "mileage": None,
        "location_city": location_city.strip() if location_city else None,
        "location_state": location_state.strip() if location_state else None,
        "location_country": "Perú",
        "external_id": raw["id"],
    }

    auction_data = {
        "source": "superbid",
        "external_id": raw["id"],
        "lot_number": raw.get("lotNumber"),
        "title": raw.get("product", {}).get("shortDesc"),
        "description": description_html,
        "start_time": start_time,
        "end_time": end_time,
        "base_price": raw.get("offerDetail", {}).get("initialBidValue"),
        "current_price": raw.get("offerDetail", {}).get("currentMaxBid"),
        "currency": "USD",
        "visits": raw.get("visits"),
        "total_bidders": raw.get("totalBidders"),
        "total_bids": raw.get("totalBids"),
        "reserved_price": raw.get("offerDetail", {}).get("reservedPrice"),
        "bid_increment": raw.get("currentBidIncrement", {}).get("currentBidIncrement"),
        "seller_name": raw.get("store", {}).get("name"),
        "seller_company": None,  # ajustar si encuentras este dato en otro lugar
        "vehicle_id": None  # se asignará luego
    }

    return auction_data, vehicle_data
