def test_create_and_read_user(client):
    # 1. Crear usuario
    response = client.post("/users/", json={
        "username": "pytestuser",
        "email": "pytest@example.com",
        "password": "strongpass"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "pytestuser"
    assert "id" in data

    # 2. Leer usuario creado
    user_id = data["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "pytest@example.com"
