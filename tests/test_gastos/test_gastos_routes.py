from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from routes.gasto_routes import router, get_db
from services import gasto_service


app = FastAPI()
app.include_router(router)
client = TestClient(app)


def override_get_db():
    db = MagicMock()
    try:
        yield db
    finally:
        pass


app.dependency_overrides[get_db] = override_get_db


def test_listar_gastos(monkeypatch):
    monkeypatch.setattr(gasto_service, "obtener_gastos", lambda db: [])

    response = client.get("/VerGastos")

    assert response.status_code == 200
    assert response.json() == []


def test_crear_gasto(monkeypatch):
    gasto_mock = {
        "Concepto": "Comida",
        "Monto": 50.0,
        "IdCliente": 1,
        "IdCategoria": 2,
        "IdMovimiento": 1,
        "FechaMovimiento": "2026-05-27T10:00:00"
    }

    monkeypatch.setattr(gasto_service, "crear_nuevo_gasto", lambda db, gasto: gasto_mock)

    response = client.post("/CrearGasto", json={
        "Concepto": "Comida",
        "Monto": 50.0,
        "IdCliente": 1,
        "IdCategoria": 2
    })

    assert response.status_code == 200
    assert response.json()["Concepto"] == "Comida"
    assert response.json()["IdCategoria"] == 2


def test_crear_gasto_sin_categoria(monkeypatch):
    gasto_mock = {
        "Concepto": "Transporte",
        "Monto": 25.0,
        "IdCliente": 1,
        "IdCategoria": None,
        "IdMovimiento": 2,
        "FechaMovimiento": "2026-05-27T10:00:00"
    }

    monkeypatch.setattr(gasto_service, "crear_nuevo_gasto", lambda db, gasto: gasto_mock)

    response = client.post("/CrearGasto", json={
        "Concepto": "Transporte",
        "Monto": 25.0,
        "IdCliente": 1
    })

    assert response.status_code == 200
    assert response.json()["IdCategoria"] is None


def test_crear_gasto_monto_negativo():
    response = client.post("/CrearGasto", json={
        "Concepto": "Comida",
        "Monto": -10,
        "IdCliente": 1,
        "IdCategoria": 2
    })

    assert response.status_code == 422


def test_editar_gasto(monkeypatch):
    gasto_actualizado = {
        "mensaje": "Gasto actualizado"
    }

    monkeypatch.setattr(gasto_service, "actualizar_gasto_db", lambda db, id_gasto, gasto: gasto_actualizado)

    response = client.put("/EditarGasto?id_gasto=1", json={
        "Concepto": "Cena",
        "Monto": 80.0,
        "IdCliente": 1,
        "IdCategoria": 2
    })

    assert response.status_code == 200
    assert response.json()["mensaje"] == "Gasto actualizado"


def test_borrar_gasto(monkeypatch):
    monkeypatch.setattr(
        gasto_service,
        "eliminar_gasto_db",
        lambda db, id_gasto: {"mensaje": "Gasto eliminado exitosamente"}
    )

    response = client.delete("/BorrarGasto?id_gasto=1")

    assert response.status_code == 200
    assert response.json()["mensaje"] == "Gasto eliminado exitosamente"