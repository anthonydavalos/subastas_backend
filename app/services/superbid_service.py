# app/services/superbid_service.py

import io
import re
import logging
import tempfile
from typing import List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from pdf2image import convert_from_bytes
import pytesseract
from pydantic import BaseModel

# Modelos locales usados para parsear la respuesta de la API de Superbid
class _OfferDetail(BaseModel):
    currentMinBid: Optional[float]
    reservedPrice: Optional[float]

class _ProductAttachment(BaseModel):
    link: str

class _Product(BaseModel):
    thumbnailUrl: Optional[str]
    attachments: List[_ProductAttachment] = []

class _Auction(BaseModel):
    desc: Optional[str]

class SuperbidRawOffer(BaseModel):
    id: int
    endDateTime: str
    price: float
    store: dict
    offerDetail: _OfferDetail
    auction: _Auction
    offerDescription: dict
    product: _Product

# Configuración de reintentos para la sesión HTTP
def _get_http_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session

# Descarga todas las ofertas de Superbid usando su API pública
def fetch_all_offers_raw() -> List[SuperbidRawOffer]:
    url = "https://www.superbid.com.br/api/v1/public/auctions/offers"
    params = {
        "category": "all",
        "page": 1,
        "pageSize": 2000,
        "type": "active"
    }
    session = _get_http_session()
    response = session.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    offers = [SuperbidRawOffer(**item) for item in data["items"]]
    return offers

# Extrae el número de lote desde la descripción
def parse_lot_number(text: str) -> Optional[int]:
    match = re.search(r"\bLote\s+(\d+)", text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

# Intenta extraer el título desde el PDF usando OCR
def extract_title_from_pdf_url(url: str) -> Optional[str]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        images = convert_from_bytes(response.content)
        text = pytesseract.image_to_string(images[0])
        return text.strip().split("\n")[0]
    except Exception as e:
        logging.warning(f"Error extracting title from PDF {url}: {e}")
        return None

# Parsea una oferta bruta de Superbid en un diccionario de datos internos
def parse_offer(raw: SuperbidRawOffer) -> dict:
    description = raw.auction.desc or ""
    lot_number = parse_lot_number(description)

    title = None
    if raw.product.attachments:
        pdf_url = raw.product.attachments[0].link
        title = extract_title_from_pdf_url(pdf_url)

    return {
        "source": "superbid",
        "external_id": raw.id,
        "lot_number": lot_number,
        "title": title,
        "description": description,
        "start_time": None,  # No disponible en el JSON de Superbid
        "end_time": raw.endDateTime,
        "base_price": raw.price,
        "current_price": raw.offerDetail.currentMinBid,
        "reserved_price": raw.offerDetail.reservedPrice,
        "bid_increment": None,
        "currency": "BRL",
        "vehicle_id": None,
        "seller_name": raw.store.get("name"),
        "seller_company": raw.store.get("tradingName"),
    }

# Función de alto nivel para importar todas las subastas de Superbid
def import_superbid_auctions() -> List[dict]:
    raw_offers = fetch_all_offers_raw()
    parsed_offers = [parse_offer(raw) for raw in raw_offers]
    return parsed_offers
