import pytest
from unittest.mock import MagicMock, patch
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

# Importamos el router y la dependencia de base de datos directamente
from routes.movimiento_routes import router as movimiento_router, get_db

# 1. Creamos una app de FastAPI exclusiva para el entorno de pruebas
local_app = FastAPI()
local_app.include_router(movimiento_router)

# 2. Mock de la dependencia de usuario
def mock_get_current_user():
    return "josseline_test"

# Buscamos y sobreescribimos la dependencia en el router aislado
# Esto rompe de raíz cualquier interferencia con main.py
from services.auth_service import get_current_user
local_app.dependency_overrides[get_current_user] = mock_get_current_user

client = TestClient(local_app)


def test_filtrar_historial_exitoso():
    """Prueba que el endpoint responda 200 OK con filtros y credenciales válidas."""
    mock_db = MagicMock()
    mock_usuario = MagicMock()
    mock_usuario.NombreUsuario = "josseline_test"
    mock_usuario.IdCliente = 42
    mock_db.query.return_value.filter.return_value.first.return_value = mock_usuario

    local_app.dependency_overrides[get_db] = lambda: mock_db

    movimientos_simulados = [
        {"IdMovimiento": 10, "Monto": 500.0, "Concepto": "Ahorro", "FechaMovimiento": "2026-05-20"}
    ]
    
    with patch("routes.movimiento_routes.filtrar_movimientos", return_value=movimientos_simulados):
        response = client.get("/filtrar", params={
            "id_tipo": 1,
            "fecha_inicio": "2026-01-01",
            "fecha_fin": "2026-12-31"
        })
        
        assert response.status_code == 200
        assert response.json()["total"] == 1
        assert response.json()["movimientos"][0]["Concepto"] == "Ahorro"


def test_filtrar_historial_vacio():
    """Prueba el comportamiento cuando no hay registros en el rango especificado."""
    mock_db = MagicMock()
    mock_usuario = MagicMock()
    mock_usuario.IdCliente = 42
    mock_db.query.return_value.filter.return_value.first.return_value = mock_usuario

    local_app.dependency_overrides[get_db] = lambda: mock_db

    with patch("routes.movimiento_routes.filtrar_movimientos", return_value=[]):
        response = client.get("/filtrar", params={
            "id_tipo": 1,
            "fecha_inicio": "2026-01-01",
            "fecha_fin": "2026-12-31"
        })
        
        assert response.status_code == 200
        assert response.json()["total"] == 0
        assert response.json()["message"] == "No se encontraron movimientos"


def test_filtrar_historial_error_fechas():
    """Prueba que el endpoint valide correctamente que fecha_inicio no sea posterior a fecha_fin."""
    response = client.get("/filtrar", params={
        "id_tipo": 1,
        "fecha_inicio": "2026-12-31",
        "fecha_fin": "2026-01-01"
    })
    
    assert response.status_code == 400
    assert response.json()["detail"] == "La fecha_inicio no puede ser mayor que fecha_fin"


def test_filtrar_historial_usuario_no_encontrado():
    """Prueba el manejo de errores si el usuario activo no es encontrado en la BD."""
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    local_app.dependency_overrides[get_db] = lambda: mock_db

    response = client.get("/filtrar", params={
        "id_tipo": 1,
        "fecha_inicio": "2026-01-01",
        "fecha_fin": "2026-12-31"
    })
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"