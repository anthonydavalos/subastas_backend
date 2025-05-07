def test_crud_vehicle(client):
    # Crear vehículo
    response = client.post("/vehicles/", json={
        "brand": "TestBrand",
        "model": "ModelX",
        "year": 2021,
        "category": "Car",
        "subcategory": "Sedan",
        "mileage": 5000,
        "location_city": "Lima",
        "location_state": "Lima",
        "location_country": "Perú"
    })
    assert response.status_code == 201
    veh = response.json()
    vid = veh["id"]

    # Leer vehículo
    response = client.get(f"/vehicles/{vid}")
    assert response.status_code == 200
    assert response.json()["brand"] == "TestBrand"

    # Actualizar vehículo
    response = client.put(f"/vehicles/{vid}", json={"brand": "NewBrand", "model": "ModelY"})
    assert response.status_code == 200
    assert response.json()["brand"] == "NewBrand"

    # Eliminar vehículo
    response = client.delete(f"/vehicles/{vid}")
    assert response.status_code == 204
