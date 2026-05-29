from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app # Asegúrate de importar tu app principal de FastAPI
from routes.ingreso_routes import get_db

client = TestClient(app)

# Sobrescribimos la dependencia de la DB
def override_get_db():
    mock_db = MagicMock()
    yield mock_db

app.dependency_overrides[get_db] = override_get_db

@patch("routes.ingreso_routes.IngresoService.registrar")
def test_registrar_ingreso_route(mock_registrar):
    # Agregamos los campos que seguramente pide IngresoResponse
    mock_registrar.return_value = {
        "IdMovimiento": 1, 
        "Concepto": "Sueldo", 
        "Monto": 1000.0,
        "FechaMovimiento": "2026-05-29T10:00:00",
        "IdCliente": 1,
        "IdTipo": 1,
        "IdCategoria": None
    }
    payload = {
        "Concepto": "Sueldo",
        "Monto": 1000.0,
        "IdCliente": 1,
        "IdMovimiento": 1
    }

    response = client.post("/ingresos/", json=payload)
    assert response.status_code == 201

@patch("routes.ingreso_routes.IngresoService.editar")
def test_editar_ingreso_route(mock_editar):
    # Hacemos lo mismo aquí
    mock_editar.return_value = {
        "IdMovimiento": 1, 
        "Concepto": "Bono", 
        "Monto": 500.0,
        "FechaMovimiento": "2026-05-29T10:00:00",
        "IdCliente": 1,
        "IdTipo": 1,
        "IdCategoria": None
    }
    payload = {
        "Concepto": "Bono",
        "Monto": 500.0
    }

    response = client.put("/ingresos/1", json=payload)
    assert response.status_code == 200