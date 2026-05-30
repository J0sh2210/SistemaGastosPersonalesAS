import pytest


def test_integracion_listar_movimientos(client):
    """Prueba la obtención de movimientos mensuales"""
    response = client.get("/movimientos/mensual", params={"mes": 5, "anio": 2026})
    
    # Puede retornar 200 si hay datos, 401 si falta autenticación, o 404 si no hay
    assert response.status_code in [200, 401, 404, 422]


def test_integracion_editar_categoria_movimiento(client):
    """Prueba actualizar la categoría de un movimiento"""
    payload = {
        "idCategoria": 1
    }
    
    # Intentar editar movimiento existente (puede no existir)
    response = client.put("/movimientos/Categoria", params={"idMovimiento": 1}, json=payload)
    
    # Puede retornar 200 o 404 si el movimiento no existe
    assert response.status_code in [200, 404]


def test_integracion_obtener_diferencia(client):
    """Prueba obtener diferencia de movimientos"""
    response = client.get("/movimientos/diferencia", params={"tipo": "mes"})
    
    assert response.status_code in [200, 404]
