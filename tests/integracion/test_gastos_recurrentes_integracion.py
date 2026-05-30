import pytest
from datetime import date


def test_integracion_crear_gasto_recurrente(client):
    """Prueba la creación de un gasto recurrente"""
    payload = {
        "Concepto": "Suscripción Netflix",
        "Monto": 15.99,
        "IdCliente": 1,
        "FechaInicio": str(date.today()),
        "Frecuencia": "mensual"
    }
    
    response = client.post("/gastos-recurrentes/", json=payload)
    
    assert response.status_code == 200
    datos = response.json()
    assert datos["Concepto"] == "Suscripción Netflix"
    assert float(datos["Monto"]) == 15.99


def test_integracion_listar_gastos_recurrentes(client):
    """Prueba la obtención de la lista de gastos recurrentes de un cliente"""
    id_cliente = 1
    response = client.get(f"/gastos-recurrentes/{id_cliente}")
    
    assert response.status_code == 200
    datos = response.json()
    assert isinstance(datos, list)


def test_integracion_editar_gasto_recurrente(client):
    """Prueba la edición de un gasto recurrente"""
    # Crear
    payload_crear = {
        "Concepto": "Servicio Internet",
        "Monto": 40.00,
        "IdCliente": 1,
        "FechaInicio": str(date.today()),
        "Frecuencia": "mensual"
    }
    
    response_post = client.post("/gastos-recurrentes/", json=payload_crear)
    assert response_post.status_code == 200
    
    id_gasto = response_post.json()["IdGastoRecurrente"]
    
    # Editar
    payload_editar = {
        "Concepto": "Servicio Internet Premium",
        "Monto": 60.00,
        "Frecuencia": "mensual"
    }
    
    response_put = client.put(f"/gastos-recurrentes/{id_gasto}", json=payload_editar)
    
    assert response_put.status_code == 200
    datos = response_put.json()
    assert datos["Concepto"] == "Servicio Internet Premium"


def test_integracion_desactivar_gasto_recurrente(client):
    """Prueba la desactivación de un gasto recurrente"""
    # Crear
    payload = {
        "Concepto": "Seguro Auto",
        "Monto": 100.00,
        "IdCliente": 1,
        "FechaInicio": str(date.today()),
        "Frecuencia": "mensual"
    }
    
    response_post = client.post("/gastos-recurrentes/", json=payload)
    assert response_post.status_code == 200
    
    id_gasto = response_post.json()["IdGastoRecurrente"]
    
    # Desactivar
    response_put = client.put(f"/gastos-recurrentes/desactivar/{id_gasto}")
    assert response_put.status_code == 200


def test_integracion_eliminar_gasto_recurrente(client):
    """Prueba la eliminación de un gasto recurrente"""
    # Crear
    payload = {
        "Concepto": "Suscripción HBO",
        "Monto": 12.99,
        "IdCliente": 1,
        "FechaInicio": str(date.today()),
        "Frecuencia": "mensual"
    }
    
    response_post = client.post("/gastos-recurrentes/", json=payload)
    assert response_post.status_code == 200
    
    id_gasto = response_post.json()["IdGastoRecurrente"]
    
    # Eliminar
    response_delete = client.delete(f"/gastos-recurrentes/eliminar/{id_gasto}")
    assert response_delete.status_code == 200
