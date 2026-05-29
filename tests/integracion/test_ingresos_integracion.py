import pytest

def test_integracion_registrar_y_editar_ingreso(client):
    # --- PASO 1: Probar la creación real usando el procedimiento sp_RegistrarIngreso ---
    payload_nuevo = {
        "Concepto": "Bono de Integracion SRE",
        "Monto": 3500.50,
        "IdCliente": 1,
        "IdMovimiento": 999999  # Usa un IdMovimiento que no choque o dependa de tu lógica de BD
    }
    
    response_post = client.post("/ingresos/", json=payload_nuevo)
    
    # Validamos que el endpoint responda un 201 Created y devuelva los datos correctos de la BD
    assert response_post.status_code == 201
    datos_creados = response_post.json()
    assert datos_creados["Concepto"] == "Bono de Integracion SRE"
    assert float(datos_creados["Monto"]) == 3500.50
    
    # Obtenemos el ID real generado u otorgado por la Base de Datos
    id_generado = datos_creados["IdMovimiento"]

    # --- PASO 2: Probar la edición real usando sp_EditarIngreso ---
    payload_editado = {
        "Concepto": "Bono de Integracion SRE (Modificado)",
        "Monto": 4000.00
    }
    
    response_put = client.put(f"/ingresos/{id_generado}", json=payload_editado)
    
    # Validamos que la actualización impacte correctamente
    assert response_put.status_code == 200
    datos_editados = response_put.json()
    assert datos_editados["Concepto"] == "Bono de Integracion SRE (Modificado)"
    assert float(datos_editados["Monto"]) == 4000.00