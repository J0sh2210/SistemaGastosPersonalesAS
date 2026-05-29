import pytest
from unittest.mock import patch
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

# Importamos tu router de metas
from routes.meta_routes import router as meta_router

app_metas_test = FastAPI()
app_metas_test.include_router(meta_router)

client = TestClient(app_metas_test)

def test_crear_meta_exitosa():
    """Prueba que el endpoint POST /api/metas/ responda 201 Created."""
    meta_mock_respuesta = {
        "id_meta": 1, 
        "nombre_meta": "Vacaciones 2026", 
        "monto_objetivo": 1500.0
    }
    
    with patch("routes.meta_routes.crear_meta", return_value=meta_mock_respuesta):
        # JSON estructurado exactamente según tus esquemas Pydantic
        response = client.post("/api/metas/", json={
            "id_usuario": 1,
            "nombre_meta": "Vacaciones 2026",
            "monto_objetivo": 1500.0,
            "fecha_limite": "2026-12-31",
            "monto_actual": 0.0
        })
        
        assert response.status_code == status.HTTP_201_CREATED


def test_actualizar_cantidad_meta_exitosa():
    """Prueba que el endpoint PUT /api/metas/cantidad/{id_meta} responda 200 OK."""
    meta_actualizada_mock = {
        "id_meta": 10, 
        "monto_actual": 750.0, 
        "mensaje": "Cantidad actualizada"
    }

    with patch("routes.meta_routes.actualizar_cantidad_ahorro", return_value=meta_actualizada_mock):
        # Usamos 'monto_actual' como lo exige tu esquema de actualización
        response = client.put("/api/metas/cantidad/10", json={
            "monto_actual": 750.0
        })
        
        assert response.status_code == status.HTTP_200_OK


def test_eliminar_meta_exitosa():
    """Prueba que el endpoint DELETE /api/metas/{id_meta} responda 200 OK."""
    respuesta_eliminar_mock = {"detail": "Meta de ahorro eliminada exitosamente"}

    with patch("routes.meta_routes.eliminar_meta", return_value=respuesta_eliminar_mock):
        response = client.delete("/api/metas/10")
        
        assert response.status_code == status.HTTP_200_OK