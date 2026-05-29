from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_registro_usuario_datos_invalidos():
    response = client.post("/usuarios/registro", json={
        "correo": "correo_invalido",
        "password": ""
    })

    assert response.status_code in [400, 422]

def test_login_incorrecto():
    response = client.post("/usuarios/login", json={
        "correo": "fake@test.com",
        "password": "incorrecta"
    })

    assert response.status_code in [400, 401, 404, 422]

def test_obtener_perfil_sin_token():
    response = client.get("/usuarios/perfil")

    assert response.status_code in [401, 403]

def test_registro_password_vacia():
    response = client.post("/usuarios/registro", json={
        "correo": "angelica@test.com",
        "password": ""
    })

    assert response.status_code in [400, 422]