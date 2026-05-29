from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app # Importa tu instancia de FastAPI
from routes.movimiento_routes import get_db
from services.auth_service import get_current_user

client = TestClient(app)

def override_get_db():
    yield MagicMock()

def override_get_current_user():
    return "testuser"

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

@patch("routes.movimiento_routes.editar_categoria_movimiento")
def test_editar_categoria_movimiento_route(mock_editar_cat):
    # Arrange
    mock_editar_cat.return_value = "OK"
    payload = {"idCategoria": 2}

    # Act
    response = client.put("/Categoria?idMovimiento=10", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Categoría actualizada correctamente"}

@patch("routes.movimiento_routes.editar_categoria_movimiento")
def test_editar_categoria_movimiento_route_not_found(mock_editar_cat):
    # Arrange
    mock_editar_cat.return_value = "MOVIMIENTO_NO_EXISTE"
    payload = {"idCategoria": 2}

    # Act
    response = client.put("/Categoria?idMovimiento=99", json=payload)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Movimiento no encontrado"}

def test_filtrar_fechas_invalidas():
    # Act
    response = client.get("/filtrar?fecha_inicio=2026-06-01&fecha_fin=2026-05-01")

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "La fecha_inicio no puede ser mayor que fecha_fin"}