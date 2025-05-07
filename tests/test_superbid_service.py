# tests/test_superbid_service_minimal.py

import pytest
from unittest.mock import patch

# Importamos directamente la función que queremos probar
from app.services.superbid_service import import_superbid_auctions

# Creamos unos datos de ejemplo que imiten a SuperbidRawOffer.json()
MOCK_RAW_OFFERS = [
    {
        "id": 12345,
        "endDateTime": "2025-12-31T12:00:00Z",
        "price": 1000.0,
        "store": {"name": "Tienda Ejemplo", "tradingName": "Ejemplo S.A."},
        "offerDetail": {"currentMinBid": 1200.0, "reservedPrice": 1500.0},
        "auction": {"desc": "Lote 7 - Subasta prueba"},
        "offerDescription": {},
        "product": {"thumbnailUrl": None, "attachments": []},
    }
]

# Y el parse_offer debería devolvernos un dict con campos concretos
MOCK_PARSED_OFFERS = [
    {
        "source": "superbid",
        "external_id": 12345,
        "lot_number": 7,
        "title": None,
        "description": "Lote 7 - Subasta prueba",
        "start_time": None,
        "end_time": "2025-12-31T12:00:00Z",
        "base_price": 1000.0,
        "current_price": 1200.0,
        "reserved_price": 1500.0,
        "bid_increment": None,
        "currency": "BRL",
        "vehicle_id": None,
        "seller_name": "Tienda Ejemplo",
        "seller_company": "Ejemplo S.A.",
    }
]

@pytest.fixture(autouse=True)
def mock_fetch_and_parse(monkeypatch):
    # Sustituimos fetch_all_offers_raw para que devuelva nuestros RAWs
    monkeypatch.setattr(
        "app.services.superbid_service.fetch_all_offers_raw",
        lambda: MOCK_RAW_OFFERS
    )
    # Sustituimos parse_offer para que devuelva nuestro parsed
    monkeypatch.setattr(
        "app.services.superbid_service.parse_offer",
        lambda raw: MOCK_PARSED_OFFERS[0]
    )

def test_import_superbid_auctions_minimal():
    """
    import_superbid_auctions debería devolver exactamente MOCK_PARSED_OFFERS
    cuando fetch_all_offers_raw y parse_offer están mockeadas.
    """
    result = import_superbid_auctions()
    assert isinstance(result, list), "Debe retornar una lista"
    assert result == MOCK_PARSED_OFFERS
